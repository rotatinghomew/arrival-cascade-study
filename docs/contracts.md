# 业务数据与接口

arrivals 的 at 是设备给出的时间格起点，真实时刻在 [at, at+precision_seconds) 内；同一格内不同 arrival_id 不能排序为精确时序。exposure 给出不重叠的半开区间，observed=false 代表记录不可得。

events 是独立的活动日历，不由来车尖峰反推生成。events 的时间是已知计划时刻；sites 是路段设施，不代表活动发生的因果位置。可用资料的截止时刻由 catalog.cutoff 给出。

POST /v1/window-check 接收 revision、site、start、end；返回该查询与观测开放窗口的重叠秒数以及已知活动。调度端的查询是未来时间窗，不提供未来到达记录。

## 资料发布

GET /v1/catalog 返回 revision、cutoff、settings 以及表名。GET /v1/tables/表名 按 revision、offset、limit 分页。默认 31 行，最多 100 行；next=null 表示结束。错误版本返回 409，参数错误返回 400，领域查询不可计算时返回 422。资料从 JSON 加载后对当前实例不可变；重启可换一个发布版本。

所有时间均为带 +08:00 的 ISO 8601 字符串，资料窗口用半开区间，只有免费时长阈值明确包含端点。计数为非负整数；null 表示未观察或未知，不等于零。来源分页顺序不是业务先后顺序。来源参数 revision 必须与资料一致。

业务服务现有 GET /v1/summary、GET /v1/reports/标识和 GET /health。概览保留 revision 和 cutoff，store.py 对规范 JSON 计算 SHA-256，内容相同重复读取不会产生不同标识。新的研究结果可独立扩展，不应改变现有概览指标的含义。
