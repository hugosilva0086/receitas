# Tutorial Completo de Deploy - Sistema de Receitas Oftalmológicas

**Autor:** Manus AI  
**Data:** Janeiro 2025  
**Versão:** 1.0

## Introdução

Este tutorial foi criado para ensinar como fazer o deploy do Sistema de Receitas Oftalmológicas em uma VPS (Virtual Private Server). O tutorial é escrito de forma simples e detalhada, como se estivesse ensinando uma criança, com todos os passos necessários para colocar o sistema funcionando na internet.

O sistema foi desenvolvido com as seguintes tecnologias:
- **Backend:** Flask (Python)
- **Frontend:** React
- **Banco de Dados:** SQLite
- **Containerização:** Docker
- **Proxy Reverso:** Nginx

## Pré-requisitos

Antes de começar, você precisará ter:

1. **Uma VPS** com sistema operacional Linux (Ubuntu 20.04 ou superior recomendado)
2. **Acesso SSH** à sua VPS
3. **Domínio** (opcional, mas recomendado)
4. **Conhecimentos básicos** de linha de comando

### Especificações Mínimas da VPS

- **CPU:** 1 vCPU
- **RAM:** 1GB
- **Armazenamento:** 20GB SSD
- **Largura de banda:** 1TB/mês

## Passo 1: Preparando a VPS

### 1.1 Conectando à VPS

Primeiro, conecte-se à sua VPS usando SSH. Substitua `SEU_IP` pelo IP da sua VPS:

```bash
ssh root@SEU_IP
```

Ou se você tiver um usuário específico:

```bash
ssh usuario@SEU_IP
```

### 1.2 Atualizando o Sistema

Sempre comece atualizando o sistema operacional:

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3 Instalando Dependências Básicas

Instale as ferramentas necessárias:

```bash
sudo apt install -y curl wget git unzip
```

## Passo 2: Instalando o Docker

O Docker é fundamental para nosso sistema. Vamos instalá-lo passo a passo.

### 2.1 Removendo Versões Antigas (se existirem)

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

### 2.2 Instalando o Docker

```bash
# Adicionar a chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Adicionar o repositório do Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualizar o índice de pacotes
sudo apt update

# Instalar o Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 2.3 Instalando o Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2.4 Configurando Permissões

Para não precisar usar `sudo` sempre:

```bash
sudo usermod -aG docker $USER
```

**Importante:** Após executar este comando, você precisa fazer logout e login novamente, ou reiniciar a VPS.

### 2.5 Testando a Instalação

```bash
docker --version
docker-compose --version
```

Se os comandos retornarem as versões, a instalação foi bem-sucedida.



## Passo 3: Preparando os Arquivos do Sistema

### 3.1 Criando o Diretório do Projeto

Crie um diretório para o projeto:

```bash
mkdir -p /opt/receitas-oftalmologicas
cd /opt/receitas-oftalmologicas
```

### 3.2 Transferindo os Arquivos

Você pode transferir os arquivos de várias formas. Aqui estão as principais:

#### Opção A: Usando SCP (do seu computador local)

Se você tem os arquivos no seu computador, use SCP:

```bash
# Execute este comando no seu computador local, não na VPS
scp -r /caminho/para/receitas-oftalmologicas/* usuario@SEU_IP:/opt/receitas-oftalmologicas/
```

#### Opção B: Usando Git (recomendado)

Se você tem o código em um repositório Git:

```bash
git clone https://github.com/seu-usuario/receitas-oftalmologicas.git .
```

#### Opção C: Upload Manual

Você pode usar ferramentas como FileZilla ou WinSCP para fazer upload dos arquivos.

### 3.3 Verificando a Estrutura dos Arquivos

Após transferir os arquivos, verifique se a estrutura está correta:

```bash
ls -la
```

Você deve ver algo assim:

```
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── src/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── static/
├── scripts/
│   └── inserir_dados.py
└── data/
```

### 3.4 Configurando Permissões

Defina as permissões corretas:

```bash
sudo chown -R $USER:$USER /opt/receitas-oftalmologicas
chmod +x scripts/inserir_dados.py
```

## Passo 4: Configurando o Sistema

### 4.1 Criando o Diretório de Dados

O diretório `data` é onde o banco de dados será armazenado:

```bash
mkdir -p data
chmod 755 data
```

### 4.2 Configurando Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` para configurações sensíveis:

```bash
nano .env
```

Adicione o seguinte conteúdo:

```env
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
```

**Importante:** Substitua `sua_chave_secreta_muito_segura_aqui` por uma chave realmente segura.

### 4.3 Configurando o Nginx (se necessário)

Se você quiser usar HTTPS, edite o arquivo `nginx.conf`:

```bash
nano nginx.conf
```

Descomente as seções de HTTPS e configure os certificados SSL.

## Passo 5: Fazendo o Deploy

### 5.1 Construindo e Iniciando os Containers

Execute o seguinte comando para construir e iniciar o sistema:

```bash
docker-compose up -d --build
```

Este comando irá:
- Construir a imagem Docker da aplicação
- Baixar a imagem do Nginx
- Iniciar os containers em segundo plano

### 5.2 Verificando se os Containers Estão Rodando

```bash
docker-compose ps
```

Você deve ver algo assim:

```
NAME                    COMMAND                  SERVICE             STATUS              PORTS
receitas-app-1          "python src/main.py"     app                 running             0.0.0.0:5000->5000/tcp
receitas-nginx-1        "/docker-entrypoint.…"   nginx               running             0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

### 5.3 Verificando os Logs

Para ver se tudo está funcionando corretamente:

```bash
# Logs da aplicação
docker-compose logs app

# Logs do Nginx
docker-compose logs nginx

# Logs de todos os serviços
docker-compose logs
```

## Passo 6: Configurando o Firewall

### 6.1 Instalando o UFW (se não estiver instalado)

```bash
sudo apt install ufw
```

### 6.2 Configurando as Regras

```bash
# Permitir SSH (IMPORTANTE: faça isso primeiro!)
sudo ufw allow ssh

# Permitir HTTP
sudo ufw allow 80

# Permitir HTTPS
sudo ufw allow 443

# Ativar o firewall
sudo ufw enable
```

### 6.3 Verificando o Status

```bash
sudo ufw status
```

## Passo 7: Testando o Sistema

### 7.1 Testando Localmente na VPS

```bash
curl http://localhost
```

Se retornar HTML, o sistema está funcionando.

### 7.2 Testando pelo IP Público

Abra um navegador e acesse:

```
http://SEU_IP_DA_VPS
```

Você deve ver a tela de login do sistema.

### 7.3 Fazendo Login

Use as credenciais padrão:
- **Usuário:** adm
- **Senha:** 0t1c4*

**Importante:** Altere essa senha imediatamente após o primeiro login!

## Passo 8: Configurações de Produção

### 8.1 Configurando um Domínio (Opcional)

Se você tem um domínio, configure-o para apontar para o IP da sua VPS:

1. Acesse o painel do seu provedor de domínio
2. Crie um registro A apontando para o IP da VPS
3. Aguarde a propagação DNS (pode levar até 24 horas)

### 8.2 Configurando SSL/HTTPS (Recomendado)

Para usar HTTPS, você pode usar o Let's Encrypt:

```bash
# Instalar o Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Configurar renovação automática
sudo crontab -e
```

Adicione esta linha ao crontab:

```
0 12 * * * /usr/bin/certbot renew --quiet
```

### 8.3 Configurando Backup Automático

Crie um script de backup:

```bash
nano /opt/backup-receitas.sh
```

Conteúdo do script:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
PROJECT_DIR="/opt/receitas-oftalmologicas"

mkdir -p $BACKUP_DIR

# Backup do banco de dados
cp $PROJECT_DIR/data/app.db $BACKUP_DIR/app_$DATE.db

# Backup dos arquivos (opcional)
tar -czf $BACKUP_DIR/receitas_$DATE.tar.gz $PROJECT_DIR

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "app_*.db" -mtime +7 -delete
find $BACKUP_DIR -name "receitas_*.tar.gz" -mtime +7 -delete

echo "Backup realizado em $DATE"
```

Torne o script executável e configure no crontab:

```bash
chmod +x /opt/backup-receitas.sh

# Adicionar ao crontab para executar diariamente às 2h
sudo crontab -e
```

Adicione:

```
0 2 * * * /opt/backup-receitas.sh
```


## Passo 9: Gerenciamento e Manutenção

### 9.1 Comandos Úteis do Docker

```bash
# Ver containers rodando
docker-compose ps

# Parar o sistema
docker-compose down

# Iniciar o sistema
docker-compose up -d

# Reiniciar o sistema
docker-compose restart

# Ver logs em tempo real
docker-compose logs -f

# Atualizar o sistema (após mudanças no código)
docker-compose down
docker-compose up -d --build
```

### 9.2 Monitoramento do Sistema

#### Verificando o Uso de Recursos

```bash
# Uso de CPU e memória
htop

# Uso de disco
df -h

# Uso de memória
free -h

# Processos do Docker
docker stats
```

#### Verificando Logs do Sistema

```bash
# Logs do sistema
sudo journalctl -f

# Logs específicos do Docker
sudo journalctl -u docker.service
```

### 9.3 Inserindo Dados no Sistema

Use o script fornecido para inserir dados:

```bash
cd /opt/receitas-oftalmologicas
python3 scripts/inserir_dados.py
```

Ou para inserir dados de exemplo:

```bash
python3 scripts/inserir_dados.py --exemplo
```

### 9.4 Atualizando o Sistema

Quando houver atualizações no código:

1. Faça backup dos dados
2. Baixe a nova versão
3. Pare o sistema
4. Atualize os arquivos
5. Reconstrua e inicie

```bash
# Backup
cp data/app.db data/app.db.backup

# Parar sistema
docker-compose down

# Atualizar código (se usando Git)
git pull

# Reconstruir e iniciar
docker-compose up -d --build
```

## Passo 10: Solução de Problemas

### 10.1 Problemas Comuns

#### Sistema não inicia

```bash
# Verificar logs
docker-compose logs

# Verificar se as portas estão livres
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :5000
```

#### Erro de permissão no banco de dados

```bash
# Corrigir permissões
sudo chown -R 1000:1000 data/
chmod 755 data/
```

#### Container não consegue se conectar

```bash
# Verificar rede do Docker
docker network ls
docker network inspect receitas-oftalmologicas_default
```

### 10.2 Comandos de Diagnóstico

```bash
# Status dos serviços
systemctl status docker

# Espaço em disco
du -sh /opt/receitas-oftalmologicas/

# Verificar conectividade
curl -I http://localhost
ping google.com
```

### 10.3 Restaurando Backup

Se precisar restaurar um backup:

```bash
# Parar o sistema
docker-compose down

# Restaurar banco de dados
cp /opt/backups/app_YYYYMMDD_HHMMSS.db data/app.db

# Iniciar sistema
docker-compose up -d
```

## Passo 11: Segurança

### 11.1 Alterando Senhas Padrão

**MUITO IMPORTANTE:** Altere a senha do usuário administrador:

1. Acesse o sistema
2. Vá em "Usuários"
3. Crie um novo usuário administrador com senha segura
4. Delete o usuário "adm" padrão

### 11.2 Configurações de Segurança

```bash
# Desabilitar login root via SSH
sudo nano /etc/ssh/sshd_config
```

Altere:
```
PermitRootLogin no
PasswordAuthentication no  # Se usar chaves SSH
```

Reinicie o SSH:
```bash
sudo systemctl restart ssh
```

### 11.3 Atualizações de Segurança

Configure atualizações automáticas:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Passo 12: Otimização de Performance

### 12.1 Configurando Swap (se necessário)

Se sua VPS tem pouca RAM:

```bash
# Criar arquivo de swap de 2GB
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Tornar permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 12.2 Otimizando o Nginx

Edite o arquivo `nginx.conf` para adicionar cache:

```nginx
# Adicionar dentro do bloco server
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 12.3 Limpeza Regular

Crie um script de limpeza:

```bash
nano /opt/cleanup.sh
```

Conteúdo:

```bash
#!/bin/bash
# Limpar logs antigos do Docker
docker system prune -f

# Limpar logs do sistema
sudo journalctl --vacuum-time=7d

# Limpar cache do apt
sudo apt autoremove -y
sudo apt autoclean

echo "Limpeza concluída"
```

Configure para executar semanalmente:

```bash
chmod +x /opt/cleanup.sh
sudo crontab -e
```

Adicione:
```
0 3 * * 0 /opt/cleanup.sh
```

## Conclusão

Parabéns! Você configurou com sucesso o Sistema de Receitas Oftalmológicas em sua VPS. O sistema agora está:

- ✅ Rodando em containers Docker
- ✅ Acessível pela internet
- ✅ Com banco de dados persistente
- ✅ Com proxy reverso Nginx
- ✅ Com backup automático configurado
- ✅ Com monitoramento básico

### Próximos Passos Recomendados

1. **Configure HTTPS** se ainda não fez
2. **Altere todas as senhas padrão**
3. **Configure monitoramento avançado** (opcional)
4. **Teste o sistema** com dados reais
5. **Treine os usuários** no sistema

### Suporte e Manutenção

- Monitore os logs regularmente
- Mantenha o sistema atualizado
- Faça backups regulares
- Monitore o uso de recursos

### Contatos e Recursos

- **Documentação do Docker:** https://docs.docker.com/
- **Documentação do Nginx:** https://nginx.org/en/docs/
- **Documentação do Flask:** https://flask.palletsprojects.com/

---

**Desenvolvido por:** Manus AI  
**Versão do Tutorial:** 1.0  
**Data:** Janeiro 2025

Este tutorial foi criado para ser o mais completo e didático possível. Se você seguiu todos os passos, seu sistema deve estar funcionando perfeitamente. Em caso de dúvidas, revise os passos ou consulte a seção de solução de problemas.

