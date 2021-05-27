# 七段顯示器辨識

# Breakdown 分析

![image](https://user-images.githubusercontent.com/68286984/119848650-909cba00-bf3e-11eb-8b8e-1c699c4cd203.png)

# 設計

![image](https://user-images.githubusercontent.com/68286984/119848684-98f4f500-bf3e-11eb-829d-ee16faa60a5c.png)


# 框出七段數字 
1. 二值化之後，使用開運算去除白點，再用閉運算增強七段之間縫隙。
2. 找出輪廓 > 切割。

![image](https://user-images.githubusercontent.com/68286984/119842121-fe45e780-bf38-11eb-9a83-84d547d14543.png)

# Code

![image](https://user-images.githubusercontent.com/68286984/119842317-26cde180-bf39-11eb-9c9c-3f11814238a8.png)

# 穿線法
畫出豎線以及上下各兩條的橫線來判斷數字。

![image](https://user-images.githubusercontent.com/68286984/119842712-80cea700-bf39-11eb-8b20-026171144fc1.png)

# Code

![image](https://user-images.githubusercontent.com/68286984/119843046-c3907f00-bf39-11eb-93f8-b7e6b8770c88.png)

# Result

![image](https://user-images.githubusercontent.com/68286984/119843147-d7d47c00-bf39-11eb-9f08-2a41d8ba4611.png)

# 數字排序問題

1. 辨識多個七段顯示器輸出結果時，排序是照找輪廓的順序(不一定是最左邊)  ➔依照輪廓的 (x,y) 座標來判斷順序。
2. Use "imutils" 模組

![image](https://user-images.githubusercontent.com/68286984/119843557-3ef23080-bf3a-11eb-9d10-22a6cd5b4d84.png)

![image](https://user-images.githubusercontent.com/68286984/119843502-33066e80-bf3a-11eb-98f1-e57e92a5dfbb.png)

# 問題

1. 數字 “ 1 ” 在找輪廓時，會有寬不夠的問題，導致穿線法辨識結果錯誤。
2. 假設目前辨識數字為 “ 1 ” 的情況下 : 找出輪廓  ➔ 長會是寬的2倍或更多 ➔ 依此條件時將輪廓的寬加大再輸出

![image](https://user-images.githubusercontent.com/68286984/119843757-6ea13880-bf3a-11eb-9117-8da659d8fb92.png)

# Code 

![image](https://user-images.githubusercontent.com/68286984/119843920-91cbe800-bf3a-11eb-9bce-36537131694a.png)







