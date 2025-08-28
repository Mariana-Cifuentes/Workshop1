# Workshop 1 - ETL Data Engineer

## Descripción

Este proyecto corresponde al **Workshop 1** del curso **ETL (G01)** del programa de **Ingeniería de Datos e Inteligencia Artificial**.  
Simula un reto real de entrevista técnica para un rol de **Data Engineer**, implementando un proceso ETL completo:

1. **Extract** → Lectura de un dataset de candidatos desde un archivo CSV.  
2. **Transform** → Limpieza, validación, reglas de negocio (regla *HIRED*), y construcción de un **modelo dimensional (esquema en estrella)**.  
3. **Load** → Carga de las tablas resultantes a un **Data Warehouse en MySQL**.  
4. **Reporting** → Cálculo de **KPIs** y generación de reportes a partir del DW (no directamente desde el CSV).  

---

## Modelo Dimensional (Star Schema)

El **esquema en estrella** diseñado contiene:

- **Tabla de Hechos:** `fact_selection`  
  - Contiene las métricas del proceso de selección (puntajes, estado de contratación).  
- **Tablas de Dimensión:**  
  - `dim_candidate` → Información de cada candidato.  
  - `dim_date` → Fecha normalizada (día, mes, año).  
  - `dim_country` → País de postulación.  
  - `dim_technology` → Tecnología asociada al perfil.  
  - `dim_seniority` → Nivel de seniority.  

---

## ETL Pipeline

### 1. Extract
- Archivo de entrada: `data/candidates.csv` (50k registros).  
- Exploración inicial en `notebook/eda.ipynb` (validación de nulos, duplicados, emails inválidos, etc.).

### 2. Transform
- Implementado en `src/ETL/transform.py`.  
- Reglas aplicadas:
  - Columna **`hired`**: un candidato es considerado contratado si `Code Challenge Score ≥ 7` y `Technical Interview Score ≥ 7`.  
  - Creación de dimensiones y llaves primarias.  
  - Generación de la tabla de hechos `fact_selection`.  

### 3. Load
- Implementado en `src/ETL/load.py`.  
- Carga automática en **MySQL Workbench** (`selection_dw`):  
  - Creación de tablas si no existen.  
  - Inserción de registros usando `mysql-connector-python`.  

### 4. KPIs & Reporting
- Implementados en `src/ETL/kpis.py`.  
- Métricas calculadas:  
  1. **Hiring Rate (% de contratación).**  
  2. **Promedio de puntajes (challenge e interview) por seniority.**  
  3. **Contrataciones por tecnología.**  
  4. **Contrataciones por año.**  
  5. **Contrataciones por seniority.**  
  6. **Contrataciones por país a lo largo de los años** (foco: USA, Brasil, Colombia, Ecuador).  

---

## Estructura del Repositorio

## 📂 Estructura del Repositorio

```bash
WORKSHOP1/
│── data/
│   └── candidates.csv          # Dataset original
│── notebook/
│   └── eda.ipynb               # Exploración inicial (EDA)
│── src/
│   └── ETL/
│       ├── transform.py        # Transformación y creación de modelo dimensional
│       ├── load.py             # Carga a MySQL DW
│       ├── kpis.py             # Consultas SQL y KPIs
│       └── main.py             # Orquestación ETL (Extract → Transform → Load)
│── requirements.txt            # Librerías necesarias
```

## 🛠️ Tecnologías Utilizadas

- **Jupyter Notebook** → Análisis exploratorio (EDA).
- **Python** (3.x)  
  - `pandas`, `numpy` → Transformación de datos.  
  - `mysql-connector-python` → Conexión a MySQL.      
- **MySQL Workbench** → Data Warehouse (DW).  
- **Power BI** → Visualización de KPIs e informes interactivos.  

## Decisiones Clave / Justificación

- **Uso de esquema en estrella:**  
  Elegí un **Star Schema** porque es el más utilizado en entornos de analítica empresarial. Permite consultas rápidas y fáciles de entender para usuarios de negocio, al mismo tiempo que simplifica la integración de múltiples dimensiones (candidato, fecha, país, tecnología, seniority) en torno a una tabla de hechos centralizada.  

- **Elección de MySQL Workbench como Data Warehouse:**  
  Seleccioné **MySQL** porque es un gestor de bases de datos ampliamente usado en la industria, ligero y compatible con Python mediante `mysql-connector-python`. Esto facilita la replicación del proyecto en distintos entornos sin depender de soluciones propietarias más complejas.  

- **Selección de KPIs:**  
  Los KPIs elegidos reflejan indicadores estratégicos de un proceso de selección:  
  - **Hiring Rate:** mide la eficiencia global del proceso.  
  - **Promedio de puntajes por seniority:** muestra calidad del talento contratado.  
  - **Contrataciones por tecnología, seniority y país:** aportan una visión comparativa útil para la toma de decisiones en reclutamiento.  
  - **Contrataciones por año:** permite analizar tendencias históricas.  

---

## Instalación y Ejecución

1. Clonar el repositorio:  
   ```bash
   git clone <URL_REPO>
   cd WORKSHOP1
