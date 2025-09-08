import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Dmg Graph", layout="centered")

st.markdown("""<hr style="margin-top: 3px;">
<p style='text-align: center; font-size: 12px; color: gray;'>
    Made by Caleo01 &nbsp;|&nbsp; Powered by Streamlit
</p>
""", unsafe_allow_html=True)

# 제목
st.title("실시간 데미지 계산 그래프")
st.latex(r'''\small
z = \left( \frac{{\text{공격력}^2}}{{\text{공격력} + \text{적 방어력} \cdot (1 - 방깎)}} \right)
\cdot (피증) \cdot (약점계수) \cdot (스킬계수) \cdot (치피)
''')

st.markdown("""
<style>
body {
  background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
  background-repeat: repeat;
  background-size: contain;
}
</style>
""", unsafe_allow_html=True)


# z 계산 함수
def compute_z(x, y, atk, defense, w, skill, multiplier):
    numerator = atk ** 2
    denominator = atk + defense * (1 - w * 0.01)
    return (numerator / denominator) * (1 + x * 0.01) * multiplier * (skill * 0.01) * (y * 0.01)

# 슬라이더
multiplier = st.radio("약점 계수:", [1.0, 1.1, 1.2], index=0, horizontal=True)
skill = st.slider("스킬 계수 %", 10, 800, 100, step=10)
st.markdown("---")
atk = st.slider("공격력", 0, 8000, 1000, step=10)
defense = st.slider("적 방어력", 0, 7000, 1000, step=10)
w = st.slider("방어감소 %", 0, 100, 50, step=10)
x = st.slider("피해증가 %", 0, 400, 100, step=10)
y = st.slider("치명피해 %", 0, 400, 100, step=10)


# z 값 계산
z_val = compute_z(x, y, atk, defense, w, skill, multiplier)
st.write(f"약점 계수 값: {multiplier}")
st.write(f"스킬 계수 값: {skill}")
st.markdown("---")
st.markdown(f"### 실제 데미지 (z): `{z_val:.2f}`")

# 3D
x_vals = np.linspace(0, 400, 50)
y_vals = np.linspace(0, 400, 50)
X, Y = np.meshgrid(x_vals, y_vals)
Z = compute_z(X, Y, atk, defense, w, skill, multiplier)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none', alpha=0.8)
ax.scatter(x, y, z_val, color='red', s=50, label='Data')
ax.set_xlabel('Dmg Increase (%)')
ax.set_ylabel('Crit (%)')
ax.set_zlabel('Actual Dmg')
ax.set_title(f'3D Dmg Graph (atk={atk}, def={defense}, w={w}%)')
ax.legend()

# Streamlit에 출력
st.pyplot(fig)
