import os
import uuid
import base64
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import io

class ServicoUpload:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    PERFIS_DIR = UPLOAD_DIR / "perfis"
    PRODUTOS_DIR = UPLOAD_DIR / "produtos"
    
    SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:8000')
    
    TAMANHO_MAXIMO_MB = 5
    TAMANHO_MAXIMO_BYTES = TAMANHO_MAXIMO_MB * 1024 * 1024
    
    TIPOS_PERMITIDOS = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp'
    }
    
    TAMANHOS_PERFIL = {
        'original': None,
        'medium': (400, 400),
        'thumb': (150, 150)
    }
    
    def __init__(self):
        self._garantir_diretorios()
    
    def _garantir_diretorios(self):
        self.PERFIS_DIR.mkdir(parents=True, exist_ok=True)
        self.PRODUTOS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _validar_imagem(self, dados_base64: str) -> Tuple[bool, Optional[str], Optional[bytes]]:    
        try:
            dados_binarios = base64.b64decode(dados_base64)
            
            if len(dados_binarios) > self.TAMANHO_MAXIMO_BYTES:
                tamanho_mb = len(dados_binarios) / (1024 * 1024)
                return False, f"Arquivo muito grande: {tamanho_mb:.2f}MB. Maximo: {self.TAMANHO_MAXIMO_MB}MB", None
            
            try:
                imagem = Image.open(io.BytesIO(dados_binarios))
                formato = imagem.format.lower()
                
                mime_type = f"image/{formato}"
                if mime_type not in self.TIPOS_PERMITIDOS:
                    return False, f"Tipo de arquivo nao permitido: {formato}. Use: JPEG, PNG, GIF ou WebP", None
                
                return True, None, dados_binarios
                
            except Exception as e:
                return False, f"Arquivo nao e uma imagem valida: {str(e)}", None
                
        except Exception as e:
            return False, f"Erro ao decodificar base64: {str(e)}", None
    
    def _otimizar_imagem(self, dados_binarios: bytes, tamanho: Optional[Tuple[int, int]] = None, qualidade: int = 85) -> bytes:
        imagem = Image.open(io.BytesIO(dados_binarios))
        
        if imagem.mode in ('RGBA', 'LA', 'P'):
            fundo = Image.new('RGB', imagem.size, (255, 255, 255))
            if imagem.mode == 'P':
                imagem = imagem.convert('RGBA')
            fundo.paste(imagem, mask=imagem.split()[-1] if imagem.mode in ('RGBA', 'LA') else None)
            imagem = fundo
        elif imagem.mode != 'RGB':
            imagem = imagem.convert('RGB')
        
        if tamanho:
            imagem.thumbnail(tamanho, Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        imagem.save(output, format='JPEG', quality=qualidade, optimize=True)
        return output.getvalue()
    
    def salvar_foto_perfil(self, usuario_id: str, dados_base64: str) -> Tuple[bool, Optional[str], Optional[dict]]:
        valido, erro, dados_binarios = self._validar_imagem(dados_base64)
        if not valido:
            return False, erro, None
        
        pasta_usuario = self.PERFIS_DIR / str(usuario_id)
        pasta_usuario.mkdir(parents=True, exist_ok=True)
        
        urls = {}
        
        try:
            for nome_tamanho, dimensoes in self.TAMANHOS_PERFIL.items():
                if dimensoes:
                    dados_otimizados = self._otimizar_imagem(dados_binarios, dimensoes)
                else:
                    dados_otimizados = self._otimizar_imagem(dados_binarios)
                
                nome_arquivo = f"{nome_tamanho}.jpg"
                caminho_arquivo = pasta_usuario / nome_arquivo
                
                with open(caminho_arquivo, 'wb') as f:
                    f.write(dados_otimizados)
                
                url_completa = f"{self.SERVER_URL}/uploads/perfis/{usuario_id}/{nome_arquivo}"
                urls[nome_tamanho] = url_completa
            
            return True, None, urls
            
        except Exception as e:
            return False, f"Erro ao salvar arquivo: {str(e)}", None
    
    def salvar_foto_produto(self, produto_id: str, dados_base64: str, indice: int = 0) -> Tuple[bool, Optional[str], Optional[str]]:
        valido, erro, dados_binarios = self._validar_imagem(dados_base64)
        if not valido:
            return False, erro, None
        
        pasta_produto = self.PRODUTOS_DIR / str(produto_id)
        pasta_produto.mkdir(parents=True, exist_ok=True)
        
        try:
            dados_otimizados = self._otimizar_imagem(dados_binarios, (800, 800))
            
            nome_arquivo = f"foto_{indice}.jpg"
            caminho_arquivo = pasta_produto / nome_arquivo
            
            with open(caminho_arquivo, 'wb') as f:
                f.write(dados_otimizados)
            
            # Retornar URL relativa (igual ao perfil)
            url_relativa = f"/uploads/produtos/{produto_id}/{nome_arquivo}"
            return True, None, url_relativa
            
        except Exception as e:
            return False, f"Erro ao salvar arquivo: {str(e)}", None
    
    def remover_foto_perfil(self, usuario_id: str) -> bool:
        pasta_usuario = self.PERFIS_DIR / str(usuario_id)
        
        if pasta_usuario.exists():
            try:
                for arquivo in pasta_usuario.glob("*.jpg"):
                    arquivo.unlink()
                pasta_usuario.rmdir()
                return True
            except Exception:
                return False
        
        return True
    
    def remover_fotos_produto(self, produto_id: str) -> bool:
        pasta_produto = self.PRODUTOS_DIR / str(produto_id)
        
        if pasta_produto.exists():
            try:
                for arquivo in pasta_produto.glob("*.jpg"):
                    arquivo.unlink()
                pasta_produto.rmdir()
                return True
            except Exception:
                return False
        
        return True
    
    def converter_base64_para_arquivo(self, usuario_id: str, dados_base64: Optional[bytes]) -> Optional[dict]:
        if not dados_base64:
            return None
        
        try:
            base64_string = base64.b64encode(dados_base64).decode('utf-8')
            sucesso, erro, urls = self.salvar_foto_perfil(usuario_id, base64_string)
            
            if sucesso:
                return urls
            else:
                print(f"Erro ao converter foto do usuario {usuario_id}: {erro}")
                return None
                
        except Exception as e:
            print(f"Erro ao processar foto do usuario {usuario_id}: {str(e)}")
            return None


servico_upload = ServicoUpload()

