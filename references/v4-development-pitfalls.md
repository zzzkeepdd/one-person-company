# V4量化平台 开发教训

## 核心铁律（来自本session的血泪）

### 1. 改代码前先读项目文档
V4目录下有四份规格文档：PROJECT_PLAN.md、PROJECT_LESSONS.md、specs/目录下的细分文档。
动手前必须全部读一遍——文档里写了OKX代理策略、策略质检体系、MUJI配色规范等关键信息。
本session的错误：没读文档就动手改main.py，把OKX代理优先级反转（文档写代理优先，我改成了直连优先）。

### 2. 改坏代码用git恢复，不要手术
main.py有5600行。用sed/patch做外科手术式修改极易引入遗漏和残留引用。
正确做法：`git checkout main.py` 恢复原始版本，然后只改必要的部分。
本session错误：用sed替换了三十多处，到处是残留引用，最后还是要git checkout。

### 3. 策略加载的双路径陷阱
V4有两个策略加载路径，互不认账：
- `strategy_loader.py` — 策略管理页面用，有自己的排除列表
- `main.py` 的 `StrategyManager.scan()` — 交易引擎、历史重放、实盘交易用，无过滤扫描全部.py

修改排除逻辑时必须两个路径都改。只改strategy_loader不管StrategyManager.scan()，SMC策略照样被加载去跑回测。

### 4. 不要自作主张删策略
策略文件即使有"未通过稳健性检验"标注，也不能随意移到backup。
用户选策略是基于回测结果和质检报告，不是基于代码里的自评标注。
本session错误：把8个策略全移入backup只留1个，用户立刻发现不对。

### 5. 数据缓存从V3拉
V4的data_cache是空的。回测需要数据时从V3目录（`D:\量化平台V3\data_cache\`）复制CSV文件。
