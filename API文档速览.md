# 蛋糕店 App 完整接口文档
## 一、全局统一返回格式
```json
{
  "code": 0,
  "message": "操作成功",
  "data": {}
}
```

## 二、错误码对照表
| code  | message              |
|------|----------------------|
| 0    | 操作成功             |
| 1001 | 参数不能为空         |
| 1002 | 参数格式不正确       |
| 1003 | 请求过于频繁         |
| 2001 | 请先登录             |
| 2002 | 账号或密码错误       |
| 2003 | 账号已被禁用         |
| 2004 | 验证码错误           |
| 2005 | 验证码已过期         |

---

## 三、接口列表

### 通用模块
| 接口路径    | 请求方式 | 接口说明         |
| ----------- | -------- | ---------------- |
| /api/upload | POST     | 上传单张图片     |
| /api/banner | GET      | 获取首页轮播图   |
| /api/region | GET      | 获取省市区数据   |
| /api/notice | GET      | 获取平台公告     |

### 用户模块
| 接口路径                 | 请求方式 | 接口说明     |
| ------------------------ | -------- | ------------ |
| /api/user/login          | POST     | 用户登录     |
| /api/user/info           | GET      | 获取个人信息 |
| /api/user/register       | POST     | 用户注册     |
| /api/user/reset_password | POST     | 找回登录密码 |
| /api/user/update         | POST     | 修改个人资料 |
| /api/user/logout         | POST     | 退出登录     |

### 商品模块
| 接口路径                  | 请求方式 | 接口说明     |
| ------------------------- | -------- | ------------ |
| /api/product/list         | GET      | 获取商品列表 |
| /api/product/detail       | GET      | 获取商品详情 |
| /api/product/category     | GET      | 获取商品分类 |
| /api/product/search       | GET      | 搜索商品     |
| /api/product/comments     | GET      | 获取商品评价 |
| /api/product/post_comment | POST     | 发布商品评价 |

### 购物车模块
| 接口路径         | 请求方式 | 接口说明         |
| ---------------- | -------- | ---------------- |
| /api/cart/list   | GET      | 获取购物车列表   |
| /api/cart/add    | POST     | 添加商品到购物车 |
| /api/cart/edit   | POST     | 修改购物车商品   |
| /api/cart/delete | POST     | 删除购物车商品   |

### 地址模块
| 接口路径                 | 请求方式 | 接口说明         |
| ------------------------ | -------- | ---------------- |
| /api/address/list        | GET      | 获取收货地址列表 |
| /api/address/add         | POST     | 新增收货地址     |
| /api/address/edit        | POST     | 修改收货地址     |
| /api/address/set_default | POST     | 设置默认地址     |
| /api/address/delete      | POST     | 删除收货地址     |

### 订单模块
| 接口路径                   | 请求方式 | 接口说明         |
| -------------------------- | -------- | ---------------- |
| /api/order/confirm         | GET      | 获取订单结算信息 |
| /api/order/create          | POST     | 创建订单         |
| /api/order/list            | GET      | 获取订单列表     |
| /api/order/detail          | GET      | 获取订单详情     |
| /api/order/pay             | POST     | 发起订单支付     |
| /api/order/pay_result      | GET      | 查询支付结果     |
| /api/order/cancel          | POST     | 取消订单         |
| /api/order/confirm_receive | POST     | 确认收货         |

### 优惠券模块
| 接口路径            | 请求方式 | 接口说明         |
| ------------------- | -------- | ---------------- |
| /api/coupon/my      | GET      | 我的优惠券       |
| /api/coupon/receive | POST     | 领取优惠券       |
| /api/coupon/list    | GET      | 可领取优惠券列表 |

### 配送模块
| 接口路径                | 请求方式 | 接口说明       |
| ----------------------- | -------- | -------------- |
| /api/delivery/calculate | GET      | 计算配送费用   |
| /api/delivery/area      | GET      | 获取可配送范围 |

### 售后模块
| 接口路径           | 请求方式 | 接口说明     |
| ------------------ | -------- | ------------ |
| /api/refund/apply  | POST     | 申请退款     |
| /api/refund/list   | GET      | 退款记录列表 |
| /api/refund/detail | GET      | 退款详情     |

### 蛋糕定制模块
| 接口路径           | 请求方式 | 接口说明     |
| ------------------ | -------- | ------------ |
| /api/custom/apply  | POST     | 提交蛋糕定制 |
| /api/custom/list   | GET      | 我的定制订单 |
| /api/custom/detail | GET      | 定制订单详情 |

### 收藏足迹模块
| 接口路径             | 请求方式 | 接口说明       |
| -------------------- | -------- | -------------- |
| /api/collect/list    | GET      | 我的收藏列表   |
| /api/collect/operate | POST     | 收藏或取消收藏 |
| /api/footprint/list  | GET      | 浏览足迹记录   |

---

## 四、可复用接口
| 接口路径              | 可复用场景                            |
| --------------------- | ------------------------------------- |
| /api/upload           | 头像上传 评价图片 退款凭证 定制参考图 |
| /api/region           | 新增地址 编辑地址 配送区域校验        |
| /api/product/list     | 首页展示 分类页 搜索结果页            |
| /api/product/detail   | 商品详情 购物车展示 订单商品展示      |
| /api/address/list     | 订单结算 地址管理 支付页选择地址      |
| /api/order/pay_result | 支付页面 订单列表 订单详情            |
| /api/config           | 全页面通用配置                        |
