import torch
import torch.nn as nn


# 損失関数で求めた誤差を各パラメータに逆伝搬して損失に対する勾配を求め、勾配に従いパラメータを更新する. 

linear_model = nn.Linear(1, 1)

x = torch.ones(10, 1)
linear_model(x)
print(linear_model)

t_c = torch.tensor([0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0])
t_u = torch.tensor([35.7, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4])

