# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/28 19:09


# 库
import pandas as pd
import numpy as np


data = table_t001
days_table = pd.value_counts(data.uesr_id)  # 各自天数
days_table = pd.DataFrame(days_table)
days_table = days_table.reset_index()
days_table.columns = ["uesr_id", "days"]

data = data.groupby("uesr_id").sum()
data = data.sort_values("amt", ascending=False)
print("用户名", data.index[0], "金额",data.amt[0],
      "购买天数",days_table[days_table.uesr_id==data.index[0]]["days"].values, "购买金额最大")

print("用户名", days_table.uesr_id[0], "金额", data.amt[data.index==days_table.uesr_id[0]].values,
      "购买天数",days_table.days[0], "购买天数最多")