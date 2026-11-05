/* A small WASI preview-1 host with an in-memory file system, for running compiled C in a page's worker.
   Nothing here touches the visitor's disk or network. Only what a teaching program needs is implemented;
   every other import answers ENOSYS. */
export class Exit extends Error {
  constructor(code) { super(`exit ${code}`); this.code = code; }
}
const E = { SUCCESS: 0, BADF: 8, EXIST: 20, INVAL: 28, IO: 29, ISDIR: 31, NOENT: 44, NOSYS: 52, NOTDIR: 54 };
const FILETYPE = { CHARDEV: 2, DIR: 3, FILE: 4 };
const encoder = new TextEncoder();
const decoder = new TextDecoder();

export class MemFS {
  constructor() { this.files = new Map(); this.dirs = new Set(['/']); }
  mkdirs(path) {
    const parts = path.split('/').filter(Boolean);
    let at = '';
    for (const p of parts) { at += `/${p}`; this.dirs.add(at); }
  }
  write(path, data) {
    this.mkdirs(path.split('/').slice(0, -1).join('/'));
    this.files.set(path, typeof data === 'string' ? encoder.encode(data) : data);
  }
  read(path) { return this.files.get(path); }
  isDir(path) { return this.dirs.has(path === '' ? '/' : path); }
}

function normal(base, rel) {
  const parts = (rel.startsWith('/') ? rel : `${base}/${rel}`).split('/');
  const out = [];
  for (const p of parts) {
    if (!p || p === '.') continue;
    if (p === '..') out.pop(); else out.push(p);
  }
  return `/${out.join('/')}`;
}

export function runWasi(module, { args = [], fs, cwd = '/', stdin = '', env = {}, onStdout, onStderr, limitBytes = 262144 }) {
  let memory;
  const view = () => new DataView(memory.buffer);
  const bytes = () => new Uint8Array(memory.buffer);
  const stdinBytes = encoder.encode(stdin);
  let stdinPos = 0;
  let written = 0;
  const fds = new Map([
    [0, { kind: 'stdin' }], [1, { kind: 'out', sink: onStdout }], [2, { kind: 'out', sink: onStderr }],
    [3, { kind: 'dir', path: '/', preopen: '/' }],
  ]);
  let next = 4;
  const str = (ptr, len) => decoder.decode(bytes().subarray(ptr, ptr + len));
  const argBytes = args.map((a) => encoder.encode(`${a}\0`));
  const envBytes = Object.entries(env).map(([k, v]) => encoder.encode(`${k}=${v}\0`));
  const listSizes = (list, countPtr, sizePtr) => {
    view().setUint32(countPtr, list.length, true);
    view().setUint32(sizePtr, list.reduce((n, b) => n + b.length, 0), true);
    return E.SUCCESS;
  };
  const listGet = (list, ptrs, buf) => {
    let at = buf;
    list.forEach((b, i) => { view().setUint32(ptrs + i * 4, at, true); bytes().set(b, at); at += b.length; });
    return E.SUCCESS;
  };
  const filestat = (buf, type, size) => {
    const v = view();
    for (let i = 0; i < 64; i += 8) v.setBigUint64(buf + i, 0n, true);
    v.setUint8(buf + 16, type);
    v.setBigUint64(buf + 32, BigInt(size), true);
    return E.SUCCESS;
  };
  const host = {
    args_sizes_get: (c, s) => listSizes(argBytes, c, s),
    args_get: (p, b) => listGet(argBytes, p, b),
    environ_sizes_get: (c, s) => listSizes(envBytes, c, s),
    environ_get: (p, b) => listGet(envBytes, p, b),
    proc_exit: (code) => { throw new Exit(code); },
    sched_yield: () => E.SUCCESS,
    random_get: (ptr, len) => { crypto.getRandomValues(bytes().subarray(ptr, ptr + Math.min(len, 65536))); return E.SUCCESS; },
    clock_res_get: (_, ptr) => { view().setBigUint64(ptr, 1000000n, true); return E.SUCCESS; },
    clock_time_get: (id, _, ptr) => {
      const ms = id === 0 ? Date.now() : performance.now();
      view().setBigUint64(ptr, BigInt(Math.round(ms)) * 1000000n, true);
      return E.SUCCESS;
    },
    fd_prestat_get: (fd, ptr) => {
      const f = fds.get(fd);
      if (!f || !f.preopen) return E.BADF;
      view().setUint8(ptr, 0);
      view().setUint32(ptr + 4, encoder.encode(f.preopen).length, true);
      return E.SUCCESS;
    },
    fd_prestat_dir_name: (fd, ptr, len) => {
      const f = fds.get(fd);
      if (!f || !f.preopen) return E.BADF;
      bytes().set(encoder.encode(f.preopen).subarray(0, len), ptr);
      return E.SUCCESS;
    },
    fd_fdstat_get: (fd, ptr) => {
      const f = fds.get(fd);
      if (!f) return E.BADF;
      const v = view();
      v.setUint8(ptr, f.kind === 'dir' ? FILETYPE.DIR : f.kind === 'file' ? FILETYPE.FILE : FILETYPE.CHARDEV);
      v.setUint16(ptr + 2, 0, true);
      v.setBigUint64(ptr + 8, 0xffffffffn, true);
      v.setBigUint64(ptr + 16, 0xffffffffn, true);
      return E.SUCCESS;
    },
    fd_fdstat_set_flags: () => E.SUCCESS,
    fd_filestat_get: (fd, ptr) => {
      const f = fds.get(fd);
      if (!f) return E.BADF;
      if (f.kind === 'file') return filestat(ptr, FILETYPE.FILE, f.data.length);
      return filestat(ptr, f.kind === 'dir' ? FILETYPE.DIR : FILETYPE.CHARDEV, 0);
    },
    path_filestat_get: (fd, _, pathPtr, pathLen, ptr) => {
      const f = fds.get(fd);
      if (!f) return E.BADF;
      const p = normal(f.path || cwd, str(pathPtr, pathLen));
      if (fs.isDir(p)) return filestat(ptr, FILETYPE.DIR, 0);
      const file = fs.read(p);
      return file ? filestat(ptr, FILETYPE.FILE, file.length) : E.NOENT;
    },
    path_open: (dirfd, _, pathPtr, pathLen, oflags, __, ___, ____, fdPtr) => {
      const dir = fds.get(dirfd);
      if (!dir) return E.BADF;
      const p = normal(dir.path || cwd, str(pathPtr, pathLen));
      const CREAT = 1; const DIRECTORY = 2; const EXCL = 4; const TRUNC = 8;
      if (fs.isDir(p)) {
        const fd = next++;
        fds.set(fd, { kind: 'dir', path: p });
        view().setUint32(fdPtr, fd, true);
        return E.SUCCESS;
      }
      if (oflags & DIRECTORY) return E.NOTDIR;
      let data = fs.read(p);
      if (data && (oflags & EXCL)) return E.EXIST;
      if (!data && !(oflags & CREAT)) return E.NOENT;
      if (!data || (oflags & TRUNC)) { data = new Uint8Array(0); fs.write(p, data); }
      const fd = next++;
      fds.set(fd, { kind: 'file', path: p, data, pos: 0 });
      view().setUint32(fdPtr, fd, true);
      return E.SUCCESS;
    },
    path_unlink_file: (dirfd, ptr, len) => {
      const dir = fds.get(dirfd);
      if (!dir) return E.BADF;
      return fs.files.delete(normal(dir.path || cwd, str(ptr, len))) ? E.SUCCESS : E.NOENT;
    },
    path_create_directory: (dirfd, ptr, len) => {
      const dir = fds.get(dirfd);
      if (!dir) return E.BADF;
      fs.mkdirs(normal(dir.path || cwd, str(ptr, len)));
      return E.SUCCESS;
    },
    fd_close: (fd) => {
      if (!fds.has(fd)) return E.BADF;
      fds.delete(fd);
      return E.SUCCESS;
    },
    fd_seek: (fd, offset, whence, ptr) => {
      const f = fds.get(fd);
      if (!f || f.kind !== 'file') return f ? E.INVAL : E.BADF;
      const off = Number(offset);
      const at = whence === 0 ? off : whence === 1 ? f.pos + off : f.data.length + off;
      if (at < 0) return E.INVAL;
      f.pos = at;
      view().setBigUint64(ptr, BigInt(at), true);
      return E.SUCCESS;
    },
    fd_tell: (fd, ptr) => {
      const f = fds.get(fd);
      if (!f || f.kind !== 'file') return f ? E.INVAL : E.BADF;
      view().setBigUint64(ptr, BigInt(f.pos), true);
      return E.SUCCESS;
    },
    fd_read: (fd, iovs, count, ptr) => {
      const f = fds.get(fd);
      if (!f) return E.BADF;
      if (f.kind === 'dir') return E.ISDIR;
      let total = 0;
      const v = view();
      for (let i = 0; i < count; i += 1) {
        const buf = v.getUint32(iovs + i * 8, true);
        const len = v.getUint32(iovs + i * 8 + 4, true);
        if (f.kind === 'stdin') {
          const n = Math.min(len, stdinBytes.length - stdinPos);
          bytes().set(stdinBytes.subarray(stdinPos, stdinPos + n), buf);
          stdinPos += n; total += n;
        } else if (f.kind === 'file') {
          const n = Math.max(0, Math.min(len, f.data.length - f.pos));
          bytes().set(f.data.subarray(f.pos, f.pos + n), buf);
          f.pos += n; total += n;
        }
      }
      v.setUint32(ptr, total, true);
      return E.SUCCESS;
    },
    fd_write: (fd, iovs, count, ptr) => {
      const f = fds.get(fd);
      if (!f) return E.BADF;
      if (f.kind === 'dir') return E.ISDIR;
      let total = 0;
      const v = view();
      for (let i = 0; i < count; i += 1) {
        const buf = v.getUint32(iovs + i * 8, true);
        const len = v.getUint32(iovs + i * 8 + 4, true);
        const chunk = bytes().slice(buf, buf + len);
        total += len;
        if (f.kind === 'out') {
          written += len;
          if (written > limitBytes) throw new Exit(-2);
          f.sink?.(chunk);
        } else if (f.kind === 'file') {
          const end = f.pos + len;
          if (end > f.data.length) {
            const grown = new Uint8Array(end);
            grown.set(f.data);
            f.data = grown;
            fs.write(f.path, grown);
          }
          f.data.set(chunk, f.pos);
          f.pos = end;
        }
      }
      v.setUint32(ptr, total, true);
      return E.SUCCESS;
    },
  };
  const imports = {};
  for (const { module: mod, name, kind } of WebAssembly.Module.imports(module)) {
    if (kind !== 'function') continue;
    imports[mod] ??= {};
    imports[mod][name] = host[name] ?? (() => E.NOSYS);
  }
  const instance = new WebAssembly.Instance(module, imports);
  memory = instance.exports.memory;
  try {
    instance.exports._start();
    return 0;
  } catch (error) {
    if (error instanceof Exit) return error.code;
    throw error;
  }
}
