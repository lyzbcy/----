# LeetCode 380: O(1) 时间插入、删除和获取随机元素

## 核心难题
我们需要设计一个数据结构，支持以下三个操作，且时间复杂度必须都是 **O(1)**（平均情况）：
1.  `insert(val)`: 插入一个元素。
2.  `remove(val)`: 删除一个元素。
3.  `getRandom()`: 随机返回一个元素。

## 为什么难？
- **数组 (Array)**：
    - `getRandom` 是 O(1) 的（通过下标访问）。
    - `insert` 在末尾是 O(1) 的。
    - ❌ 但是 `remove` 任意元素通常是 O(N) 的，因为删除中间元素后，后面的元素都要向前移动。
- **哈希表 (HashMap / Set)**：
    - `insert` 和 `remove` 都是 O(1) 的。
    - ❌ 但是 `getRandom` 是 O(N) 的，因为哈希表没有索引，无法直接随机访问。

## 解决方案：数组 + 哈希表
我们将两者的优点结合起来：
1.  **动态数组 (`nums`)**：存储实际的数值。这让我们能用 `Math.random()` 生成索引来实现 O(1) 的 `getRandom`。
2.  **哈希表 (`valMap`)**：存储 `数值 -> 数组索引` 的映射。这让我们能在 O(1) 时间内找到某个数字在数组中的位置。

## 关键技巧：Swap and Pop (交换并删除)
这是解决 `remove` 操作 O(1) 的核心技巧。

当我们想删除数组中间的某个元素 `val` 时：
1.  我们**不能**直接删除它，否则后面的元素会移动，导致 O(N)。
2.  **技巧**：我们将要删除的元素 `val` 与数组**最后一个元素** `lastVal` **交换位置**（或者直接用 `lastVal` 覆盖 `val`）。
3.  现在，要删除的元素跑到了数组末尾。
4.  我们直接删除数组末尾的元素（`pop` 操作），这是 O(1) 的。
5.  **别忘了更新哈希表**：因为 `lastVal` 被移动到了原来 `val` 的位置，我们需要更新 `valMap` 中 `lastVal` 的索引。

## 代码逻辑详解

### 1. Insert(val)
- 检查 `val` 是否已存在（查 Map）。若存在则返回 `false`。
- 将 `val` 添加到数组 `nums` 的**末尾**。
- 在 `valMap` 中记录：`val -> (nums.length - 1)`。
- 返回 `true`。

### 2. Remove(val)
- 检查 `val` 是否存在。若不存在则返回 `false`。
- **获取位置**：从 `valMap` 中拿到 `val` 的索引 `index`。
- **获取末尾元素**：拿到 `nums` 最后一个元素 `lastVal`。
- **移动 (Swap)**：
    - 将 `nums[index]` 修改为 `lastVal`。
    - 更新 `valMap`：`lastVal` 的新索引变成了 `index`。
- **删除 (Pop)**：
    - 从 `nums` 中移除最后一个元素。
    - 从 `valMap` 中移除 `val`。
- 返回 `true`。

### 3. GetRandom()
- 生成一个随机索引：`randomIndex = Math.floor(Math.random() * nums.length)`。
- 返回 `nums[randomIndex]`。

---
**现在，请打开 `index.html` 亲自试一试！**
通过可视化的动画，你会非常清楚地看到“交换并删除”是如何发生的。
