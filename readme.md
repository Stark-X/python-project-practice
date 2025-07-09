from functools import lru_cache

# Python 项目的实践

## 代码例子

打开 [jupyter notebook](./main.ipynb) 查看

## 依赖注入

- 功能解耦
- 实现依赖缓存，避免重复创建、销毁资源
- 功能 接口/基类 注入，符合里氏替换原则
- 方便测试、替换实现

fastapi 提供了依赖注入能力 [依赖项](https://fastapi.tiangolo.com/zh/tutorial/dependencies/#_3)

```python
from abc import ABCMeta, abstractmethod
from functools import lru_cache

from app import router
from fastapi import Depends


class Interface(metaclass=ABCMeta):
    @abstractmethod
    def do_something(self) -> str:
        pass


class FooService(Interface):
    def do_something(self) -> str:
        # call others api code here
        return "do something real"


@lru_cache
def get_foo_service() -> FooService:
    return FooService()


@router.get("/api/v1/test")
def some_test(svc: Interface = Depends(get_foo_service)):
    svc.do_something()


class MockedFoo(Interface):
    """won't call another api implementation"""

    def do_something(self) -> str:
        return "do something fake"


##### pytest case ####
def test_some_test():
    actual = some_test(MockedFoo())
    assert actual == "do something fake"
```

## reformat && lint

使用 Rust 编写的 [ruff](https://docs.astral.sh/ruff/) 格式化代码

### 优势

- 代码风格一致
- 速度飞快
- 支持使用 pyproject.toml 配置
- 具备 lint 以及 reformat 的能力
- ...

### Pycharm

1. 安装插件 `ruff`
2. 关闭 `Optimzie import` 使用 Pycharm 自带的，开启 ruff format
     - NOTED. 插件提供的 `Optimzie import` 在 `__init__.py` 文件中使用时，可能会导致“未被使用”的 "import" 被移除

![ruff settings on Pycharm](img.png)

## 类型提示(type hint) && 静态类型检查

```python
from typing import Iterator

foo: Iterator = iter(range(100))
bar: list[str] = list()
```

新语法：
- `typing.Optional[str]` -> `str | None`
- `typing.List[str]` -> `list[str]`
- `typing.Dict[str, Any]` -> `dict[str, Any]`

### Optional

- 有较重的代码洁癖可以使用 [basedpyright](https://docs.basedpyright.com/latest/) 执行静态类型检查
- 电脑性能还带得动的安装 SonarQube 插件，提示常见错误

## git

### git commit 检查

使用 [pre-commit](https://pre-commit.com/#install) 安装 git hook，提前交做固定的检查

- 文件末尾空行去除
- lint(ruff)
- 代码规范问题自动修复(ruff)

### [Conventional Commit](https://www.conventionalcommits.org/zh-hans/v1.0.0/)

使用 [czg](https://cz-git.qbb.sh/zh/cli/) 交互式提交代码