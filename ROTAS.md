Aqui está a documentação detalhada das rotas do backend, incluindo a estrutura da request e da resposta em JSON:

# API Documentation

## `/genai` - POST

### Descrição

Endpoint para interagir com o serviço GenAI.

### Request

```json
{
	"username": "string",
	"password": "string",
	"prompt": "string"
}
```

### Response

```json
{
	"response": "object"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"prompt": "Recommend some games"
}
```

#### Response

```json
{
	"response": [
		{
			"command": "Recommend",
			"titles": ["Game1", "Game2"],
			"other": []
		}
	]
}
```

## `/uploadaudio` - POST

### Descrição

Endpoint para fazer upload de um arquivo de áudio e convertê-lo para texto.

### Request

- Form-data com um arquivo de áudio.

### Response

```json
{
	"text": "string"
}
```

### Exemplo

#### Request

- Form-data com um arquivo de áudio nomeado `audio`.

#### Response

```json
{
	"text": "Recognized text from audio"
}
```

## `/signup` - POST

### Descrição

Endpoint para registrar um novo usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"email": "string",
	"birthdate": "YYYY-MM-DD"
}
```

### Response

```json
{
	"message": "User signed up successfully!"
}
```

ou

```json
{
	"error": "There was an error signing up!"
}
```

### Exemplo

#### Request

```json
{
	"username": "newuser",
	"password": "password123",
	"email": "newuser@Exemplo.com",
	"birthdate": "1990-01-01"
}
```

#### Response

```json
{
	"message": "User signed up successfully!"
}
```

## `/login` - POST

### Descrição

Endpoint para fazer login de um usuário.

### Request

```json
{
	"username": "string",
	"password": "string"
}
```

### Response

```json
{
	"username": "string",
	"birthdate": "YYYY-MM-DD"
}
```

ou

```json
{
	"error": "Failed to Login"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123"
}
```

#### Response

```json
{
	"username": "user1",
	"birthdate": "1990-01-01"
}
```

## `/removeuser` - POST

### Descrição

Endpoint para remover um usuário.

### Request

```json
{
	"username": "string",
	"password": "string"
}
```

### Response

```json
{
	"success": "User removed successfully"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123"
}
```

#### Response

```json
{
	"success": "User removed successfully"
}
```

## `/changepassword` - POST

### Descrição

Endpoint para mudar a senha de um usuário.

### Request

```json
{
	"username": "string",
	"oldPassword": "string",
	"newPassword": "string"
}
```

### Response

```json
{
	"success": "Password changed successfully"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"oldPassword": "oldpassword123",
	"newPassword": "newpassword123"
}
```

#### Response

```json
{
	"success": "Password changed successfully"
}
```

## `/addtags` - POST

### Descrição

Endpoint para adicionar tags a um usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"text": "string",
	"tag_type": "string"
}
```

### Response

```json
{
	"success": "Tag added successfully"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"text": "RPG",
	"tag_type": "genre"
}
```

#### Response

```json
{
	"success": "Tag added successfully"
}
```

## `/removetags` - POST

### Descrição

Endpoint para remover tags de um usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"text": "string"
}
```

### Response

```json
{
	"success": "Tag removed successfully"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"text": "RPG"
}
```

#### Response

```json
{
	"success": "Tag removed successfully"
}
```

## `/gettags` - POST

### Descrição

Endpoint para obter as tags de um usuário.

### Request

```json
{
	"username": "string",
	"password": "string"
}
```

### Response

```json
{
	"tags": {
		"genre": ["RPG", "Action"],
		"platform": ["PC", "Console"]
	}
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123"
}
```

#### Response

```json
{
	"tags": {
		"genre": ["RPG", "Action"],
		"platform": ["PC", "Console"]
	}
}
```

## `/getrecommendations` - POST

### Descrição

Endpoint para obter recomendações de jogos para um usuário.

### Request

```json
{
	"username": "string",
	"password": "string"
}
```

### Response

```json
{
	"recommendations": [
		{
			"title": "Game1",
			"data": "object"
		},
		{
			"title": "Game2",
			"data": "object"
		}
	]
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123"
}
```

#### Response

```json
{
	"recommendations": [
		{
			"title": "Game1",
			"data": {
				"description": "An exciting RPG game",
				"rating": 4.5
			}
		},
		{
			"title": "Game2",
			"data": {
				"description": "A thrilling action game",
				"rating": 4.0
			}
		}
	]
}
```

## `/removegamefromrecommendations` - POST

### Descrição

Endpoint para remover um jogo das recomendações.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string"
}
```

### Response

```json
{
	"success": "Game removed from recommendations"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1"
}
```

#### Response

```json
{
	"success": "Game removed from recommendations"
}
```

## `/addgametolibrary` - POST

### Descrição

Endpoint para adicionar um jogo à biblioteca do usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string"
}
```

### Response

```json
{
	"success": "Game added to library"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1"
}
```

#### Response

```json
{
	"success": "Game added to library"
}
```

## `/getlibrary` - GET

### Descrição

Endpoint para obter a biblioteca de jogos do usuário.

### Request

- Parâmetro de consulta: `username`

### Response

```json
{
	"library": [
		{
			"title": "Game1",
			"data": "object",
			"rating": 4.5,
			"state": "completed"
		},
		{
			"title": "Game2",
			"data": "object",
			"rating": 4.0,
			"state": "playing"
		}
	]
}
```

### Exemplo

#### Request

```
/getlibrary?username=avnc2005
```

#### Response

```json
{
	"library": [
		{
			"title": "Game1",
			"data": {
				"description": "An exciting RPG game",
				"rating": 4.5
			},
			"rating": 4.5,
			"state": "completed"
		},
		{
			"title": "Game2",
			"data": {
				"description": "A thrilling action game",
				"rating": 4.0
			},
			"rating": 4.0,
			"state": "playing"
		}
	]
}
```

## `/removegamefromlibrary` - POST

### Descrição

Endpoint para remover um jogo da biblioteca do usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string"
}
```

### Response

```json
{
	"success": "Game removed from library"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1"
}
```

#### Response

```json
{
	"success": "Game removed from library"
}
```

## `/updaterating` - POST

### Descrição

Endpoint para atualizar a classificação de um jogo na biblioteca do usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string",
	"rating": "number"
}
```

### Response

```json
{
	"success": "Rating updated"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1",
	"rating": 4.5
}
```

#### Response

```json
{
	"success": "Rating updated"
}
```

## `/updatestate` - POST

### Descrição

Endpoint para atualizar o estado de um jogo na biblioteca do usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string",
	"state": "string"
}
```

### Response

```json
{
	"success": "State updated"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1",
	"state": "completed"
}
```

#### Response

```json
{
	"success": "State updated"
}
```

## `/gameratings` - GET

### Descrição

Endpoint para obter as classificações de um jogo.

### Request

- Parâmetro de consulta: `title`

### Response

```json
[
rating1 :int,
rating2
]
```

ou

```json
{
	"error": "Game not found"
}
```

### Exemplo

#### Request

- Parâmetro de consulta: `title=Game1`

#### Response

```json
[
rating1,
rating2,
rating3
]
```

## `/blacklistgame` - POST

### Descrição

Endpoint para adicionar um jogo ao não recomende do usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string"
}
```

### Response

```json
{
	"success": "Game blacklisted"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1"
}
```

#### Response

```json
{
	"success": "Game blacklisted"
}
```

## `/unblacklistgame` - POST

### Descrição

Endpoint para remover um jogo do não recomende do usuário.

### Request

```json
{
	"username": "string",
	"password": "string",
	"title": "string"
}
```

### Response

```json
{
	"success": "Game unblacklisted"
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123",
	"title": "Game1"
}
```

#### Response

```json
{
	"success": "Game unblacklisted"
}
```

## `/getblacklist` - POST

### Descrição

Endpoint para obter ao não recomende do usuário.

### Request

```json
{
	"username": "string",
	"password": "string"
}
```

### Response

```json
{
	["GameTitle1", "GameTitle2"]
}
```

ou

```json
{
	"error": "User not logged in"
}
```

### Exemplo

#### Request

```json
{
	"username": "user1",
	"password": "password123"
}
```

#### Response

```json
{
	["Game1", "Game2"]
}
```
