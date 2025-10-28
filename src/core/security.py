"""Arquivo responsável por lidar com as questões de autenticação da aplicação"""

import uuid
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field

from .config import settings


class TokenData(BaseModel):
    """Schema para retornar o ID do usuário contido no token JWT"""

    user_id: Optional[str] = Field(None, description="ID do usuário")


oauth2_scheme = HTTPBearer()


def decode_access_token(token: str) -> TokenData:
    """Método que decodifica o token JWT passado na header das requisições"""

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível validar as credenciais",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(user_id=user_id)
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


def get_current_user_id(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> uuid.UUID:
    """Método que retorna o ID do usuário contido no token JWT passado na header"""

    token = creds.credentials
    token_data = decode_access_token(token)
    return uuid.UUID(token_data.user_id)
