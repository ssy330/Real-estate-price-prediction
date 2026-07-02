import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = r"D:\캡스톤"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_CRS = "EPSG:5181"

# 행정동 경계 shapefile 불러오기
dong = gpd.read_file(
    os.path.join(BASE_DIR, "bnd_dong_11_2025_2Q.shp")
)

# 필요한 컬럼만 남기기
dong = dong[["ADM_CD", "ADM_NM", "geometry"]].copy()

# 좌표계 통일
dong = dong.to_crs(TARGET_CRS)

print("=== 행정동 경계 데이터 ===")
print(dong.head())
print("행정동 CRS:", dong.crs)
print("행정동 개수:", len(dong))
print("행정동 bounds:", dong.total_bounds)

# 중간 산출물 저장
commercial_df = pd.read_csv(
    os.path.join(BASE_DIR, "상업편의시설_전처리.csv"),
    encoding="cp949"
)

hospital_df = pd.read_csv(
    os.path.join(BASE_DIR, "병원_전처리.csv"),
    encoding="cp949"
)

print("\n=== CSV 불러오기 완료 ===")
print("commercial:", commercial_df.shape)
print("hospital:", hospital_df.shape)

# GeoDataFrame 변환
# 상업시설 (x, y)
commercial_gdf = gpd.GeoDataFrame(
    commercial_df.copy(),
    geometry=gpd.points_from_xy(commercial_df["x"], commercial_df["y"]),
    crs=TARGET_CRS
)

hospital_gdf = gpd.GeoDataFrame(
    hospital_df.copy(),
    geometry=gpd.points_from_xy(hospital_df["x"], hospital_df["y"]),
    crs=TARGET_CRS
)

# 좌표계 및 범위 확인
print("\n=== GeoDataFrame CRS 확인 ===")
print("dong:", dong.crs)
print("commercial:", commercial_gdf.crs)
print("culture:", hospital_gdf.crs)

print("\n=== bounds 확인 ===")
print("dong:", dong.total_bounds)
print("commercial:", commercial_gdf.total_bounds)
print("hospital:", hospital_gdf.total_bounds)


# 중간 산출물 저장 (GeoJSON)
commercial_gdf.to_file(
    os.path.join(OUTPUT_DIR, "commercial.geojson"),
    driver="GeoJSON"
)

hospital_gdf.to_file(
    os.path.join(OUTPUT_DIR, "hospital.geojson"),
    driver="GeoJSON"
)

print("\n=== GeoJSON 저장 완료 ===")
print(os.path.join(OUTPUT_DIR, "commercial.geojson"))
print(os.path.join(OUTPUT_DIR, "hospital.geojson"))


# 1차 시각화 검증
fig, axes = plt.subplots(2, 3, figsize=(16, 14))
axes = axes.flatten()

plot_items = [
    ("상업시설", commercial_gdf, "red"),
    ("병원", hospital_gdf, "blue"),
]

for ax, (title, gdf, color) in zip(axes, plot_items):
    dong.plot(ax=ax, color="white", edgecolor="black", linewidth=0.2)
    gdf.plot(ax=ax, color=color, markersize=3, alpha=0.7)
    ax.set_title(f"행정동 경계 + {title}")
    ax.axis("off")

plt.tight_layout()
plt.show()

print("\n01_make_geodata.py 실행 완료")