"""
Análisis de Churn - Empresa de Suscripción (tipo Netflix)
Objetivo: Entender por qué los clientes se van y cuáles se quedan

Workflow: Leer CSV -> Visualizar -> Analizar -> Limpiar -> Exportar XLSX
"""
import pandas as pd

# =============================================================================
# 1. LEER ARCHIVO CSV
# =============================================================================
dt = pd.read_csv("clientes_churn_proyecto.csv")

# =============================================================================
# 2. VISUALIZAR LA BASE DE DATOS (columnas, tipos, estructura)
# =============================================================================
print("=" * 60)
print("VISUALIZACIÓN INICIAL DE LA BASE DE DATOS")
print("=" * 60)

print("\n1. Columnas y tipos de datos:")
print(dt.dtypes)

print("\n2. Primeras filas:")
print(dt.head())

print("\n3. Resumen estadístico:")
print(dt.describe())

print("\n4. Valores nulos por columna:")
print(dt.isnull().sum())

# =============================================================================
# 3. ANALIZAR - Resultados que coinciden con Resultado_de_Analisis.txt
# =============================================================================
print("\n" + "=" * 60)
print("ANÁLISIS DE CHURN (10 Preguntas)")
print("=" * 60)

# -----------------------------------------------------------------------------
# PREGUNTA 1: ¿Cuál es la tasa general de churn?
# -----------------------------------------------------------------------------
churn_si = dt[dt["Churn"] == 1].shape[0]
churn_no = dt[dt["Churn"] == 0].shape[0]
total = len(dt)
print("\n--- PREGUNTA 1: Tasa general de churn ---")
print(f"   - Clientes que se fueron (Churn=1): {churn_si} ({churn_si/total*100:.1f}%)")
print(f"   - Clientes que se quedaron (Churn=0): {churn_no} ({churn_no/total*100:.1f}%)")
print(f"   - Total clientes: {total}")

# -----------------------------------------------------------------------------
# PREGUNTA 2: ¿Qué plan tiene mayor tasa de abandono?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 2: Churn por Plan ---")
churn_plan = dt.groupby("Plan")["Churn"].agg(
    clientes_total="count",
    clientes_churn="sum",
    tasa_churn=lambda x: (x.sum()/len(x)*100).round(1)
).sort_values("tasa_churn", ascending=True)
print(churn_plan)

# -----------------------------------------------------------------------------
# PREGUNTA 3: ¿Qué región tiene más clientes que se van?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 3: Churn por Región ---")
churn_region = dt.groupby("Region")["Churn"].agg(
    clientes_total="count",
    clientes_churn="sum",
    tasa_churn=lambda x: (x.sum()/len(x)*100).round(1)
).sort_values("tasa_churn", ascending=True)
print(churn_region)

# -----------------------------------------------------------------------------
# PREGUNTA 4: ¿Los que se van tienen menos meses activos?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 4: Meses activo (Churn vs No Churn) ---")
meses_comparacion = dt.groupby("Churn")["Meses_Activo"].agg(
    promedio_meses="mean",
    cantidad="count"
).round(2)
print(meses_comparacion)

# -----------------------------------------------------------------------------
# PREGUNTA 5: ¿El uso de la app influye en el churn?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 5: Uso de app - horas (Churn vs No Churn) ---")
uso_comparacion = dt.groupby("Churn")["Uso_App_Horas"].agg(
    promedio_horas="mean",
    cantidad="count"
).round(2)
print(uso_comparacion)

# -----------------------------------------------------------------------------
# PREGUNTA 6: ¿Los que contactan más a soporte se van más?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 6: Contactos con soporte (Churn vs No Churn) ---")
soporte_comparacion = dt.groupby("Churn")["Soporte_Contactos"].agg(
    promedio_contactos="mean",
    cantidad="count"
).round(2)
print(soporte_comparacion)

# -----------------------------------------------------------------------------
# PREGUNTA 7: ¿La edad influye en el churn?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 7: Edad promedio (Churn vs No Churn) ---")
edad_comparacion = dt.groupby("Churn")["Edad"].agg(
    edad_promedio="mean",
    cantidad="count"
).round(2)
print(edad_comparacion)

# -----------------------------------------------------------------------------
# PREGUNTA 8: ¿Qué combinación Plan + Región tiene mayor churn?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 8: Combinación Plan + Región (mayor churn) ---")
combinacion = dt.groupby(["Plan", "Region"])["Churn"].agg(
    total="count",
    churn="sum",
    tasa=lambda x: (x.sum()/len(x)*100).round(1)
).sort_values("tasa", ascending=False)
print(combinacion.head(10))

# -----------------------------------------------------------------------------
# PREGUNTA 9: ¿Por qué se van los clientes? (Síntesis - sin resultado numérico)
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 9: ¿Por qué se van? ---")
print("   (Síntesis en Resultado_de_Analisis.txt - factores: Región Norte, Plan,")
print("   edad joven, uso intensivo, precio $20)")

# -----------------------------------------------------------------------------
# PREGUNTA 10: ¿El precio del plan influye?
# -----------------------------------------------------------------------------
print("\n--- PREGUNTA 10: Churn por Precio Mensual ---")
churn_precio = dt.groupby("Precio_Mensual")["Churn"].agg(
    clientes_total="count",
    clientes_churn="sum",
    tasa_churn=lambda x: (x.sum()/len(x)*100).round(1)
).sort_values("tasa_churn", ascending=True)
print(churn_precio)

# =============================================================================
# 4. LIMPIAR Y PREPARAR LA BASE DE DATOS
# =============================================================================
print("\n" + "=" * 60)
print("LIMPIEZA Y PREPARACIÓN")
print("=" * 60)

# Copia para exportar (no modificar dt original del análisis)
dt_limpio = dt.copy()

# Eliminar valores nulos (si existieran)
dt_limpio = dt_limpio.dropna()
print(f"\n- Valores nulos eliminados. Filas restantes: {len(dt_limpio)}")

# Eliminar columna Cliente_ID (exportar sin ID según reglas)
dt_limpio = dt_limpio.drop("Cliente_ID", axis=1)
print("- Columna Cliente_ID eliminada (exportación sin ID)")

# Agregar columnas útiles para el análisis
dt_limpio["Rango_Edad"] = dt_limpio["Edad"].apply(
    lambda x: "18-30" if x <= 30 else ("31-45" if x <= 45 else "46-64")
)
dt_limpio["Uso_App_Alto"] = dt_limpio["Uso_App_Horas"].apply(
    lambda x: "Alto" if x > 50 else "Bajo"
)
dt_limpio["Estado_Cliente"] = dt_limpio["Churn"].apply(
    lambda x: "Se fue" if x == 1 else "Se quedó"
)
print("- Columnas agregadas: Rango_Edad, Uso_App_Alto, Estado_Cliente")

# =============================================================================
# 5. DESCARGAR ARCHIVO EN FORMATO XLSX
# =============================================================================
dt_limpio.to_excel("Data_analysis.xlsx", index=False)
print(f"\n- Archivo exportado: Data_analysis.xlsx ({len(dt_limpio)} filas)")

print("\n" + "=" * 60)
print("FIN DEL ANÁLISIS")
print("=" * 60)
