# 麻布餃子API

白金高輪にある四川料理屋さんのメニュー情報を提供するAPIです。

APIの詳細はこちらをご覧ください。

https://azabu-gyoza-api.herokuapp.com/

食べログは[こちら](https://tabelog.com/tokyo/A1307/A130702/13142179/)


## エンドポイント

### お酒なし（for Member）

**カテゴリー情報**

1件取得

> /api/category/{id}

複数取得

> /api/category

**メニュー情報**

1件取得

> /api/menu/{id}

複数取得

> /api/menu


### お酒あり（for Mentor）

**カテゴリー情報**

1件取得

> /api/v1/category/{id}

複数取得

> /api/v1/category

**メニュー情報**

1件取得

> /api/v1/menu/{id}

複数取得

> /api/v1/menu


## クエリパラメータ

|パラメータ| 必須  | 備考  |
|:---:|:---:|:---:|
|name|     |メニュー名で部分一致検索ができます。|
|category_id|     | 指定したカテゴリーIDのメニューを返します。 |
|price|     | 指定された金額のメニューを返します。 |

