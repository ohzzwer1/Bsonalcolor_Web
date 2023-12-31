# -*- coding: utf-8 -*-
"""bsonalcolor_real.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ilQZyzR-OBE0wzBfKc6NyU5dZJbzPk3Q

# Noise 제거

### 파일 읽기
"""

import pandas as pd
import math

color = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'purple', 'white']
colordf = []
for c in color:
    file_path = "/Users/yubin/Bsonalcolor/Bsonalcolor_web/pylsl/examples/" + c + ".csv"
    df = pd.read_csv(file_path, sep='|', header=None, names=['Timestamp', 'Values', 'NaN'])
    df = df.drop(columns=['NaN'])

    df_values = df['Values'].apply(lambda x: pd.Series(eval(x)))
    df = pd.concat([df['Timestamp'], df_values], axis=1)
    df.columns = ['Timestamp', 'TP9', 'AF7', 'AF8', 'TP10', 'aux']
    df['Timestamp']=df['Timestamp']-df['Timestamp'][0]

    df['Time'] = df['Timestamp'].apply(lambda x: math.floor(x))
    df['Data'] = df[['TP9', 'AF7', 'AF8', 'TP10', 'aux']].values.tolist()
    df['Label'] = color.index(c)
    start_timestamp = df['Time'].iloc[0]
    df = df.drop(['Data', 'Time', 'TP9', 'TP10', 'aux'], axis=1)
    colordf.append(df)
    c = df

df = pd.concat(colordf)

"""### fft"""
import numpy as np

# FFT 변환 계산 및 결과 추가 코드
def calculate_fft(column):
    y = df[column].values
    n = len(y)
    k = np.arange(n)
    T = n * df['Timestamp'].diff().mean()
    freq = k / T
    freq = freq[range(int(n/2))]
    Y = np.fft.fft(y) / n
    return abs(Y[:n//2])

# 'TP9', 'AF7', 'AF8', 'TP10', 'aux' 각 열에 대해 FFT 변환 계산 및 결과 추가
columns = ['AF7', 'AF8']
for column in columns:
    fft_result = calculate_fft(column)
    df[f'{column}_FFT'] = np.concatenate([fft_result, np.zeros(len(df) - len(fft_result))])

"""### filtering
- IQR
- 주파수
"""
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# 대역 통과 필터 설계 함수
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# 대역 통과 필터 적용 함수
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# 주어진 데이터프레임 열에 대역 통과 필터를 적용
def apply_bandpass_filter(df, column_name, lowcut, highcut, fs, wave, order=5):
    data = df[column_name].values
    filtered_data = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    df[column_name + '_'+wave+'_filtered'] = filtered_data
    return df

# 세타파 필터링 함수
def theta(column, df_filtered):

    lowcut = 4.0  # 최저 주파수 (Hz)
    highcut = 8.0  # 최고 주파수 (Hz)
    fs = len(df_filtered['Timestamp'])/(df_filtered['Timestamp'][df_filtered['Timestamp'].size-1]-df_filtered['Timestamp'][0])

    df_filtered = apply_bandpass_filter(df_filtered, column+'_FFT', lowcut, highcut, fs, 'theta')

    # 시각화
    # plt.figure(figsize=(60,8))
    # plt.plot(df_filtered[:int(df_filtered[column+'_FFT_theta_filtered'].size/2)][column+'_FFT_theta_filtered'], label='Filtered Data')
    # plt.title(column+' theta brainwave')
    # plt.legend()
    # plt.show()
    return df_filtered[column+'_FFT_theta_filtered']

# SMR파 필터링 함수
def SMR(column,df_filtered):

    lowcut = 12.0  # 최저 주파수 (Hz)
    highcut = 15.0  # 최고 주파수 (Hz)
    fs = len(df_filtered['Timestamp'])/(df_filtered['Timestamp'][df_filtered['Timestamp'].size-1]-df_filtered['Timestamp'][0])

    df_filtered = apply_bandpass_filter(df_filtered, column+'_FFT', lowcut, highcut, fs, 'SMR')

    # 시각화
    # plt.figure(figsize=(60,8))
    # plt.plot(df_filtered[:int(df_filtered[column+'_FFT_SMR_filtered'].size/2)][column+'_FFT_SMR_filtered'], label='Filtered Data')
    # plt.title(column+' SMR brainwave')
    # plt.legend()
    # plt.show()
    return df_filtered[column+'_FFT_SMR_filtered']

# mid-bet파 필터링 함수
def mid_beta(column,df_filtered):

    lowcut = 15.0  # 최저 주파수 (Hz)
    highcut = 18.0  # 최고 주파수 (Hz)
    fs = len(df_filtered['Timestamp'])/(df_filtered['Timestamp'][df_filtered['Timestamp'].size-1]-df_filtered['Timestamp'][0])

    df_filtered = apply_bandpass_filter(df_filtered, column+'_FFT', lowcut, highcut, fs, 'mid_beta')

    # 시각화
    # plt.figure(figsize=(60,8))
    # plt.plot(df_filtered[:int(df_filtered[column+'_FFT_mid_beta_filtered'].size/2)][column+'_FFT_mid_beta_filtered'], label='Filtered Data')
    # plt.title(column+' mid beta brainwave')
    # plt.legend()
    # plt.show()
    return df_filtered[column+'_FFT_mid_beta_filtered']

# 이상치 데이터 제거
q99_value = df['AF7_FFT'].quantile(0.99)
q1_value = df['AF7_FFT'].quantile(0.01)

df_filtered = df[(df[column+'_FFT'] >= q1_value) & (df[column+'_FFT'] <= q99_value)]
df_filtered=df_filtered.reset_index().drop('index', axis=1)

df = df_filtered
df['AF7_FFT_theta_filtered'] = theta('AF7', df)
df['AF7_FFT_SMR_filtered'] = SMR('AF7', df)
df['AF7_FFT_mid_beta_filtered'] = mid_beta('AF7', df)
# print(df.columns)
# print(df['AF7_FFT_mid_beta_filtered'])

"""### 집중도"""

def get_con(f):
    concentrate = (f['AF7_FFT_mid_beta_filtered'] + f['AF7_FFT_SMR_filtered'])/f['AF7_FFT_theta_filtered']
    concentrate.dropna(inplace=True)

    q99_value = concentrate.quantile(0.99)
    q1_value = concentrate.quantile(0.01)

    # IQR을 기반으로 이를 벗어나는 데이터 제거
    concentrate = concentrate[(concentrate >= q1_value) & (concentrate <= q99_value)]
    return concentrate

result = {}
dfs = []
for i in df['Label'].unique().tolist():
    dfs.append(df[df['Label']==i])

for i in range(8):
    con = get_con(dfs[i])
    result[color[i]]=[np.mean(con)]

result = pd.DataFrame.from_dict(result).T.reset_index()
result = result.rename(columns={0:'concentrate', 'index':'color'})

conc = result['concentrate'].tolist()
new_con = []
for c in conc:
    if c>0:
        new_con.append(math.log10(c))
    elif c<0:
        new_con.append(-math.log10(-c))
    else: new_con.append(0)
print(new_con)
# plt.title("concentration")
# plt.bar(result['color'], result['concentrate'])