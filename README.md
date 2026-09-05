# Learn-github
![Version](https://img.shields.io/badge/version-0.0.1-blue)

something for github

## Math API(四则运算 HTTP 计算 API)

启动入口 `main.py` 后,本程序提供四条 GET 计算接口(不再输出问候内容):

| 接口 | 参数 | 成功响应(200) | 失败响应(400) |
|---|---|---|---|
| `GET /add` | `a`、`b`(数字) | `{"result": 和}` | 见下方错误说明 |
| `GET /subtract` | `a`、`b`(数字) | `{"result": 差}` | 见下方错误说明 |
| `GET /multiply` | `a`、`b`(数字) | `{"result": 积}` | 见下方错误说明 |
| `GET /divide` | `a`、`b`(数字) | `{"result": 商}` | 见下方错误说明 |

- 参数支持整数、小数、负数与科学计数法;结果以 JSON number 输出,遵循 IEEE 754 双精度浮点语义。
- 参数缺失或无法解析为数字:返回 `400` 与 `{"error": "invalid parameters"}`。
- 除法接口除数为 0:返回 `400` 与 `{"error": "division by zero"}`;其余接口不受此限制。
- 请求中的未知参数被忽略;接口无状态、无持久化、无需认证。

### 运行方式

```sh
pip install -r requirements.txt
python main.py
```

服务默认监听 http://127.0.0.1:5000,例如:

```sh
curl "http://127.0.0.1:5000/add?a=2&b=3"
# {"result":5.0}
```

### 测试

```sh
pytest -q
```

### 示例脚本

问候与 Person 类示例已迁移至 `examples/` 目录,内容与运行行为保持不变:

- `examples/Hello_Dad.py`
- `examples/Hello_GitHub.py`
- `examples/Hello_Mom.py`
- `examples/Person.py`
