彩色分等级日志。结论一律 `print` 走 stdout，内部诊断走这里走 stderr。
统一用单例 `Log`，不要在业务模块里再实例化，否则一份日志散到两个实例、等级各调各的。
打开 DEBUG：CLI `--verbose` 或环境变量 `XMYZ_VERBOSE=1`。
