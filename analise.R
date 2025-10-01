# analise.R (com diagnósticos para garantir saída)
options(echo = TRUE)  # ecoa as linhas executadas

cat("Working dir:", getwd(), "\n")

csv_path <- "culturas.csv"
cat("CSV alvo:", csv_path, "\n")

if (!file.exists(csv_path)) {
  stop("ERRO: CSV não encontrado. Exporte pelo Python (menu [5]) e rode de novo.")
}

dados <- read.csv(csv_path, stringsAsFactors = FALSE)
cat("Linhas lidas:", nrow(dados), "\n")

media_area <- tapply(dados$area_m2, dados$cultura, mean, na.rm = TRUE)
dp_area    <- tapply(dados$area_m2, dados$cultura, sd,   na.rm = TRUE)

media_kg   <- tapply(dados$kg_necessarios, dados$cultura, mean, na.rm = TRUE)
dp_kg      <- tapply(dados$kg_necessarios, dados$cultura, sd,   na.rm = TRUE)

cat("\n=== ÁREA (m²) por cultura ===\n")
for (c in names(media_area)) {
  cat(sprintf("- %s: média = %.2f | desvio-padrão = %.2f\n",
              c, media_area[[c]], dp_area[[c]]))
}

cat("\n=== INSUMO (kg) por cultura ===\n")
for (c in names(media_kg)) {
  cat(sprintf("- %s: média = %.2f | desvio-padrão = %.2f\n",
              c, media_kg[[c]], dp_kg[[c]]))
}

cat("\nPronto!\n")
