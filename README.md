# 🛰️ IoT Edge Simulator — MQTT + InfluxDB + Grafana

Simulador de dispositivos IoT com processamento de borda, coleta via MQTT e visualização de dados em tempo real via Grafana.

---

## 🚀 Arquitetura

A arquitetura é composta pelos seguintes serviços (orquestrados via Docker Compose):

| Serviço           | Descrição | Porta |
|-------------------|------------|-------|
| **Mosquitto**     | Broker MQTT para comunicação dos dispositivos. | `1883` |
| **Device Sim**    | Simulador de dispositivos publicando mensagens no MQTT. | - |
| **Edge Processor**| Processa as mensagens de borda (inference/modelo, pré-processamento etc). | - |
| **Result Logger** | Escuta mensagens e armazena resultados processados. | - |
| **InfluxDB**      | Banco de dados de séries temporais. | `8086` |
| **Telegraf**      | Coletor MQTT → InfluxDB (pipeline de dados). | - |
| **Grafana**       | Painel de visualização e análise em tempo real. | `3000` |

---

## ⚙️ Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 📦 Configuração

1. Copie o arquivo `.env.example` e renomeie para `.env`:

   ```bash
   cp .env.example .env
