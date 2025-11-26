import numpy as np
import pandas as pd

# Исходные данные
U = 11  # В
psi_U = 30  # градусов
R1 = 29  # Ом
Rk = 15  # Ом
C = 23.974e-6  # Ф
L = 21.422e-3  # Гн
f0 = 222.085  # Гц

# Расчет характеристического сопротивления и добротности
rho = np.sqrt(L / C)
Qp = rho / (R1 + Rk)

print(f"Характеристическое сопротивление ρ = {rho:.3f} Ом")
print(f"Расчетная добротность Qp = {Qp:.3f}")

# Создание массива частот от 0.1*f0 до 2*f0
frequencies = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                       1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]) * f0

# Функции для расчетов
def calculate_phase_shift(f, R1, Rk, L, C):
    """Расчет фазового сдвига φ"""
    omega = 2 * np.pi * f
    XL = omega * L
    XC = 1 / (omega * C)
    X = XL - XC
    R_total = R1 + Rk
    phi_rad = np.arctan2(X, R_total)
    return np.degrees(phi_rad)

def calculate_current(f, U, R1, Rk, L, C):
    """Расчет тока I"""
    omega = 2 * np.pi * f
    XL = omega * L
    XC = 1 / (omega * C)
    R_total = R1 + Rk
    Z = np.sqrt(R_total**2 + (XL - XC)**2)
    return U / Z

def calculate_UR1(I, R1):
    """Расчет напряжения на R1"""
    return I * R1

def calculate_Uk(f, I, Rk, L):
    """Расчет напряжения на катушке"""
    omega = 2 * np.pi * f
    XL = omega * L
    return I * np.sqrt(Rk**2 + XL**2)

def calculate_UC(f, I, C):
    """Расчет напряжения на конденсаторе"""
    omega = 2 * np.pi * f
    XC = 1 / (omega * C)
    return I * XC

# Расчет данных для всех частот
results = []

for f in frequencies:
    # Расчетные значения
    phi_calc = calculate_phase_shift(f, R1, Rk, L, C)
    I_calc = calculate_current(f, U, R1, Rk, L, C)
    UR1_calc = calculate_UR1(I_calc, R1)
    Uk_calc = calculate_Uk(f, I_calc, Rk, L)
    UC_calc = calculate_UC(f, I_calc, C)
    
    # Для экспериментальных значений можно добавить измеренные данные
    # Пока оставим пустыми или равными расчетным
    phi_exp = phi_calc  # Заменить на экспериментальные данные
    I_exp = I_calc      # Заменить на экспериментальные данные
    UR1_exp = UR1_calc  # Заменить на экспериментальные данные
    Uk_exp = Uk_calc    # Заменить на экспериментальные данные
    UC_exp = UC_calc    # Заменить на экспериментальные данные
    
    results.append({
        'f_ratio': f / f0,
        'f_Hz': f,
        'phi_calc': phi_calc,
        'I_calc': I_calc,
        'UR1_calc': UR1_calc,
        'Uk_calc': Uk_calc,
        'UC_calc': UC_calc,
        'phi_exp': phi_exp,
        'I_exp': I_exp,
        'UR1_exp': UR1_exp,
        'Uk_exp': Uk_exp,
        'UC_exp': UC_exp
    })

# Создание DataFrame
df = pd.DataFrame(results)

# Форматирование вывода
pd.set_option('display.precision', 3)

print("\n" + "="*80)
print(f"{'Таблица 2.3':^80}")
print("="*80)
print(f"U = {U} [В]; R1 = {R1} [Ом]; Rk = {Rk} [Ом]; L = {L*1000:.3f} [мГн]; C = {C*1e6:.3f} [мкФ]")
print(f"f0 = {f0:.3f} [Гц]")
print(f"{'Расчет':^40}{'Эксперимент':^40}")
print(f"Qp = {Qp:.5f}\t\t\tQe = {Qp:.5f}")  # Qe заменить на экспериментальное значение

print("\n" + "-"*120)
print(f"{'f':<10} {'φ расч':<8} {'I расч':<8} {'UR1 расч':<8} {'Uk расч':<8} {'UC расч':<8} "
      f"{'φ эксп':<8} {'I эксп':<8} {'UR1 эксп':<8} {'Uk эксп':<8} {'UC эксп':<8}")
print(f"{'[Гц]':<10} {'[°]':<8} {'[А]':<8} {'[В]':<8} {'[В]':<8} {'[В]':<8} "
      f"{'[°]':<8} {'[А]':<8} {'[В]':<8} {'[В]':<8} {'[В]':<8}")
print("-"*120)

for _, row in df.iterrows():
    print(f"{row['f_ratio']:.1f}·f0  {row['phi_calc']:>7.2f} {row['I_calc']:>7.3f} {row['UR1_calc']:>7.3f} "
          f"{row['Uk_calc']:>7.3f} {row['UC_calc']:>7.3f}   {row['phi_exp']:>7.2f} {row['I_exp']:>7.3f} "
          f"{row['UR1_exp']:>7.3f} {row['Uk_exp']:>7.3f} {row['UC_exp']:>7.3f}")

# Дополнительные расчеты для примера (f = 0.1*f0)
print("\n" + "="*80)
print("Пример расчета для f = 0.1·f0:")
print("="*80)

f_example = 0.1 * f0
phi_example = calculate_phase_shift(f_example, R1, Rk, L, C)
I_example = calculate_current(f_example, U, R1, Rk, L, C)
UR1_example = calculate_UR1(I_example, R1)
Uk_example = calculate_Uk(f_example, I_example, Rk, L)
UC_example = calculate_UC(f_example, I_example, C)

print(f"f = {f_example:.3f} Гц")
print(f"φ = arctg(X/R) = {phi_example:.2f}°")
print(f"I = U/Z = {I_example:.3f} А")
print(f"UR1 = I·R1 = {UR1_example:.3f} В")
print(f"Uk = I·√(Rk² + (ωL)²) = {Uk_example:.3f} В")
print(f"UC = I/(ωC) = {UC_example:.3f} В")

# Сохранение в файл
df.to_csv('rlc_circuit_analysis.csv', index=False, encoding='utf-8-sig')
print(f"\nДанные сохранены в файл 'rlc_circuit_analysis.csv'")