# YouTube Downloader v3.0

Aplicação modular para download de vídeos e áudios do YouTube, refatorada seguindo as melhores práticas de programação.

## 🏗️ Arquitetura

A aplicação foi completamente reestruturada seguindo os princípios SOLID, DRY e KISS:

### Estrutura de Diretórios

```
src/
├── config/          # Configurações e constantes
│   ├── __init__.py
│   └── settings.py  # Configurações centralizadas
├── models/          # Modelos de dados
│   ├── __init__.py
│   └── download_result.py  # Classes de dados para resultados
├── services/        # Lógica de negócio
│   ├── __init__.py
│   ├── ffmpeg_manager.py      # Gerenciamento do FFmpeg
│   ├── youtube_downloader.py  # Serviço principal de download
│   └── playlist_handler.py    # Manipulação de playlists
├── ui/              # Interface de usuário
│   ├── __init__.py
│   ├── input_handler.py  # Coleta de entrada do usuário
│   └── menu.py          # Exibição de menus e relatórios
├── utils/           # Utilitários
│   ├── __init__.py
│   ├── validators.py   # Validação de URLs e entrada
│   ├── file_utils.py   # Manipulação de arquivos
│   └── logger.py      # Sistema de logging com cores
├── core/            # Núcleo da aplicação
│   ├── __init__.py
│   └── app.py       # Aplicação principal
└── __init__.py
```

## 🎯 Princípios Aplicados

### SOLID

1. **Single Responsibility Principle (SRP)**

   - Cada classe tem uma única responsabilidade
   - `FFmpegManager`: Apenas gerencia FFmpeg
   - `YouTubeDownloader`: Apenas faz downloads
   - `PlaylistHandler`: Apenas manipula playlists

2. **Open/Closed Principle (OCP)**

   - Classes abertas para extensão, fechadas para modificação
   - Interfaces bem definidas para adicionar novos tipos de download

3. **Liskov Substitution Principle (LSP)**

   - Subclasses podem substituir suas classes base sem quebrar funcionalidade

4. **Interface Segregation Principle (ISP)**

   - Interfaces pequenas e específicas
   - Clientes não dependem de interfaces que não usam

5. **Dependency Inversion Principle (DIP)**
   - Dependências injetadas via construtor
   - Código depende de abstrações, não de implementações concretas

### DRY (Don't Repeat Yourself)

- Eliminação de código duplicado
- Configurações centralizadas em `settings.py`
- Utilitários reutilizáveis em `utils/`
- Validação centralizada

### KISS (Keep It Simple, Stupid)

- Cada módulo é simples e focado
- Funções pequenas com responsabilidades claras
- Interface limpa e intuitiva

## 🚀 Funcionalidades

### Downloads

- Download único de vídeo/áudio
- Download em lote com processamento paralelo
- Suporte completo a playlists
- Verificação de arquivos existentes
- Relatórios detalhados de falhas

### Interface

- Menus interativos coloridos
- Validação robusta de entrada
- Feedback visual de progresso
- Relatórios de erro detalhados

### Configuração

- Setup automático do FFmpeg
- Configurações centralizadas e modificáveis
- Suporte a diferentes formatos de saída

## 📁 Componentes Principais

### Models (`models/`)

- `DownloadResult`: Representa o resultado de um download
- `BatchDownloadResult`: Resultado de downloads em lote
- `VideoInfo`: Informações de vídeos
- Enums para tipos e status de download

### Services (`services/`)

- `FFmpegManager`: Gerencia instalação e configuração do FFmpeg
- `YouTubeDownloader`: Lógica principal de download
- `PlaylistHandler`: Processamento de playlists

### UI (`ui/`)

- `InputHandler`: Coleta e validação de entrada do usuário
- `MenuDisplay`: Exibição de menus e relatórios
- `MenuController`: Controle do fluxo de menus

### Utils (`utils/`)

- `URLValidator`: Validação de URLs do YouTube
- `FileManager`: Operações de arquivo
- `Logger`: Sistema de logging colorido
- `ReportGenerator`: Geração de relatórios

## 🛠️ Instalação e Uso

### Requisitos

```bash
pip install -r requirements.txt
```

### Execução

```bash
python main_new.py
```

## 🔧 Configuração

As configurações podem être modificadas em `src/config/settings.py`:

```python
@dataclass
class Settings:
    MAX_PARALLEL_DOWNLOADS = 5  # Número máximo de downloads simultâneos
    DEFAULT_AUDIO_QUALITY = "192"  # Qualidade padrão do áudio
    REQUEST_TIMEOUT = 30  # Timeout para requisições
```

## 🧪 Extensibilidade

A nova arquitetura permite fácil extensão:

1. **Novos tipos de download**: Adicione novos tipos em `DownloadType`
2. **Novos serviços**: Crie novos serviços em `services/`
3. **Novas validações**: Adicione em `utils/validators.py`
4. **Novos formatos de relatório**: Estenda `ReportGenerator`

## 📊 Benefícios da Refatoração

1. **Manutenibilidade**: Código organizado e modular
2. **Testabilidade**: Componentes isolados e testáveis
3. **Reutilização**: Utilitários e serviços reutilizáveis
4. **Extensibilidade**: Fácil adição de novas funcionalidades
5. **Legibilidade**: Código mais limpo e documentado
6. **Confiabilidade**: Validação robusta e tratamento de erros

## 🔄 Migração

Para usar a nova versão modular:

1. Execute `python main_new.py` em vez de `python main.py`
2. As configurações agora estão em `src/config/settings.py`
3. Logs e relatórios são mais detalhados
4. A interface é mais intuitiva

## 🤝 Contribuição

A nova estrutura facilita contribuições:

- Cada módulo é independente
- Testes podem ser escritos por componente
- Documentação está integrada ao código
- Princípios SOLID garantem código limpo
