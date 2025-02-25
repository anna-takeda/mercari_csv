import streamlit as st
import pandas as pd

def main():
    st.title("CSVアップロード＆転記アプリ")

    st.write("倉庫革命CSV(warehouse.csv)をアップロード")
    warehouse_file = st.file_uploader("倉庫革命CSVを選択", type="csv")

    st.write("メルカリ(またはorder.csv)をアップロード")
    order_file = st.file_uploader("メルカリCSVを選択", type="csv")

    if warehouse_file is not None and order_file is not None:
        # CSVをDataFrameとして読み込む (Shift-JIS/CP932 として仮定)
        warehouse_df = pd.read_csv(warehouse_file, header=None, dtype=str, encoding="cp932").fillna("")
        order_df = pd.read_csv(order_file, header=None, dtype=str, encoding="cp932").fillna("")

        # 以下、同じ処理
        filtered_warehouse = warehouse_df[warehouse_df.iloc[:, 16] == "モックストア メルカリ店"]

        order_dict = {}
        for i in range(len(order_df)):
            col1_value = order_df.iloc[i, 0]
            last8 = col1_value[-8:] if len(col1_value) >= 8 else col1_value
            order_dict[last8] = i

        for row_idx in filtered_warehouse.index:
            w_8th = warehouse_df.iloc[row_idx, 7]
            w_8th_last8 = w_8th[-8:] if len(w_8th) >= 8 else w_8th

            if w_8th_last8 in order_dict:
                o_row = order_dict[w_8th_last8]
                w_34th_value = warehouse_df.iloc[row_idx, 33]
                order_df.iat[o_row, 14] = w_34th_value

        st.write("転記が完了しました。以下、更新後の order.csv の上部をプレビューします。")
        st.dataframe(order_df.head())

        csv = order_df.to_csv(index=False, header=False, encoding="utf-8-sig")
        st.download_button(
            label="更新後のorder.csvをダウンロード",
            data=csv,
            file_name="updated_order.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
