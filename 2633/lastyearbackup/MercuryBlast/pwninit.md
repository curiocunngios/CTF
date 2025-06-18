To install pwninit on Kali Linux, you can use cargo (Rust's package manager). Here are the steps:

1. First, install Rust and cargo if you haven't already:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

2. Source the cargo environment (or restart your terminal):
```bash
source $HOME/.cargo/env
```

3. Install pwninit:
```bash
cargo install pwninit
```

If you don't have the required dependencies, you might need to install them first:
```bash
sudo apt-get update
sudo apt-get install -y build-essential pkg-config libssl-dev
```

## Errors encountered 
```
error: failed to run custom build command for `rust-lzma v0.5.1`

Caused by:
  process didn't exit successfully: `/tmp/cargo-installPHPtOc/release/build/rust-lzma-3e28d47fca69573e/build-script-build` (exit status: 101)
  --- stdout
  cargo:rerun-if-env-changed=LIBLZMA_NO_PKG_CONFIG
  cargo:rerun-if-env-changed=PKG_CONFIG_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG
  cargo:rerun-if-env-changed=PKG_CONFIG
  cargo:rerun-if-env-changed=LIBLZMA_STATIC
  cargo:rerun-if-env-changed=LIBLZMA_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_STATIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_SYSROOT_DIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR

  --- stderr
  thread 'main' panicked at /home/kali/.cargo/registry/src/index.crates.io-6f17d22bba15001f/rust-lzma-0.5.1/build.rs:10:9:
  Could not find liblzma using pkg-config
  note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
warning: build failed, waiting for other jobs to finish...
error: failed to compile `pwninit v3.3.1`, intermediate artifacts can be found at `/tmp/cargo-installPHPtOc`.
To reuse those artifacts with a future compilation, set the environment variable `CARGO_TARGET_DIR` to that path.
```
## Fix
You need to install the lzma development library first. For Kali Linux, run:

```bash
sudo apt-get update
sudo apt-get install -y liblzma-dev
```

Then try installing pwninit again:
```bash
cargo install pwninit
```
