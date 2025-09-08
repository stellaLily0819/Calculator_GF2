import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Dmg Graph", layout="centered")

# 제목
st.title("실시간 데미지 계산 그래프")

# z 계산 함수
def compute_z(x, y, atk, defense, w, multiplier):
    numerator = atk ** 2
    denominator = atk + defense * (1 - w * 0.01)
    return (numerator / denominator) * (1 + x * 0.01) * multiplier * (100 * 0.01) * (y * 0.01)

# 슬라이더
multiplier = st.radio("약점 계수:", [1.0, 1.1, 1.2], index=0, horizontal=True)
st.write(f"선택한 계수 값: {multiplier}")
atk = st.slider("공격력", 1, 8000, 1000, step=10)
defense = st.slider("적 방어력", 1, 7000, 1000, step=10)
w = st.slider("방어감소 %", 0.0, 100.0, 50.0, step=1.0)
x = st.slider("피해증가 %", 0.0, 400.0, 100.0, step=5.0)
y = st.slider("치명피해 %", 0.0, 400.0, 100.0, step=5.0)


# z 값 계산
z_val = compute_z(x, y, atk, defense, w, multiplier)
st.markdown(f"###실제 데미지 (z): `{z_val:.2f}`")

# 3D
x_vals = np.linspace(0, 400, 50)
y_vals = np.linspace(0, 400, 50)
X, Y = np.meshgrid(x_vals, y_vals)
Z = compute_z(X, Y, atk, defense, w)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none', alpha=0.8)
ax.scatter(x, y, z_val, color='red', s=50, label='입력 값')
ax.set_xlabel('Dmg Increase (%)')
ax.set_ylabel('Crit (%)')
ax.set_zlabel('Actual Dmg')
ax.set_title(f'3D Dmg Graph (atk={atk}, def={defense}, w={w}%)')
ax.legend()

# Streamlit에 출력
st.pyplot(fig)
