from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password
from .models import Cliente
import json
import jwt
from django.conf import settings

@api_view(['GET'])
def test_api(request):
    return Response({"msg": "¡API Django funcionando correctamente!"})

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_view(request):
    try:
        data = json.loads(request.body)
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
        
        if not usuario or not contrasena:
            return Response({
                'msg': 'Usuario y contraseña son requeridos',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar el cliente por usuario_acceso
        try:
            cliente = Cliente.objects.get(usuario_acceso=usuario)
        except Cliente.DoesNotExist:
            return Response({
                'msg': 'Usuario no encontrado',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verificar la contraseña
        if not cliente.check_password(contrasena):
            return Response({
                'msg': 'Contraseña incorrecta',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'msg': 'Contraseña incorrecta',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generar tokens JWT
        refresh = RefreshToken()
        refresh['user_id'] = cliente.id
        refresh['username'] = cliente.usuario_acceso
        refresh['email'] = cliente.email
        refresh['nombre'] = cliente.nombre
        
        return Response({
            'msg': 'Login exitoso',
            'success': True,
            'token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': cliente.id,
                'username': cliente.usuario_acceso,
                'email': cliente.email,
                'nombre': cliente.nombre,
                'empresa': cliente.empresa
            }
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({
            'msg': 'Formato JSON inválido',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'msg': f'Error interno del servidor: {str(e)}',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_token(request):
    """Verificar token y obtener información del usuario"""
    try:
        # Obtener token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({
                'msg': 'Token no proporcionado',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decodificar el token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            # Buscar el cliente
            cliente = Cliente.objects.get(id=user_id)
            
            return Response({
                'msg': 'Token válido',
                'success': True,
                'user': {
                    'id': cliente.id,
                    'username': cliente.usuario_acceso,
                    'email': cliente.email,
                    'nombre': cliente.nombre,
                    'empresa': cliente.empresa
                }
            }, status=status.HTTP_200_OK)
            
        except jwt.ExpiredSignatureError:
            return Response({
                'msg': 'Token expirado',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({
                'msg': 'Token inválido',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Cliente.DoesNotExist:
            return Response({
                'msg': 'Usuario no encontrado',
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        return Response({
            'msg': f'Error al verificar token: {str(e)}',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
