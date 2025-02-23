import streamlit as st
import pandas as pd

def main():
    st.title("CSVアップロード＆転記アプリ")

    st.write("倉庫革命CSV(warehouse.csv)をアップロード")
    warehouse_file = st.file_uploader("倉庫革命CSVを選択", type="csv")

    st.write("メルカリ(またはorder.csv)をアップロード")
    order_file = st.file_uploader("メルカリCSVを選択", type="csv")

    if warehouse_file is not None and order_file is not None:
        # CSVをDataFrameとして読み込む
        warehouse_df = pd.read_csv(warehouse_file, header=None, dtype=str).fillna("")
        order_df = pd.read_csv(order_file, header=None, dtype=str).fillna("")

        # 1. 倉庫革命CSV (warehouse_df) の 17列目 が「モックストア メルカリ店」の行だけフィルタ
        #    -> 1始まりで17列目 ⇒ iloc[:, 16] (0始まり)
        filtered_warehouse = warehouse_df[ warehouse_df.iloc[:, 16] == "モックストア メルカリ店" ]

        # 2. 条件: warehouse_df の 8列目 と order_df の 1列目 の下8桁が一致
        #    -> 8列目 ⇒ iloc[:, 7], 1列目 ⇒ iloc[:, 0]
        #    下8桁比較のため、あらかじめ order側を「下8桁をキー」にした辞書で引けるように準備する
        order_dict = {}

        # order.csvの各行について、1列目(=iloc[:,0])の下8桁をキーに、行番号をバリューにする
        for i in range(len(order_df)):
            col1_value = order_df.iloc[i, 0]  # 1列目
            last8 = col1_value[-8:] if len(col1_value) >= 8 else col1_value  # 下8桁(なければその文字列全部)
            order_dict[last8] = i  # 行番号を紐付け

        # 3. 一致したら「倉庫革命CSVの 34列目 の値を order.csv の 15列目 に転記」
        #    -> 34列目 ⇒ iloc[:, 33], 15列目 ⇒ iloc[:, 14]
        for row_idx in filtered_warehouse.index:
            w_8th = warehouse_df.iloc[row_idx, 7]  # 8列目
            # 下8桁の一致をみるため、そのまま w_8th をキーに辞書を引く
            # ただし、order側は「下8桁」で引いているので w_8th 側も下8桁を取る場合は合わせる必要あり
            # (「倉庫革命の8列目が既に8桁だけを持つ」想定ならそのままでも可)
            w_8th_last8 = w_8th[-8:] if len(w_8th) >= 8 else w_8th

            if w_8th_last8 in order_dict:
                # order_df側の該当行を取得
                o_row = order_dict[w_8th_last8]

                # 倉庫革命CSVの34列目を取得
                w_34th_value = warehouse_df.iloc[row_idx, 33]

                # order_dfの15列目に代入
                order_df.iat[o_row, 14] = w_34th_value

        st.write("転記が完了しました。以下、更新後の order.csv の上部をプレビューします。")
        st.dataframe(order_df.head())

        # 更新後のorder.csvをダウンロードできるようにする
        csv = order_df.to_csv(index=False, header=False, encoding="utf-8-sig")
        st.download_button(
            label="更新後のorder.csvをダウンロード",
            data=csv,
            file_name="updated_order.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
