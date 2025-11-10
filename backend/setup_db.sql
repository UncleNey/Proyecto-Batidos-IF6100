\
-- DDL completo para SQL Server (orden correcto)
CREATE DATABASE batidos;
GO
USE batidos;
GO

CREATE TABLE categoria (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(50) NOT NULL UNIQUE
);
GO

CREATE TABLE batido (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  slug VARCHAR(100) NOT NULL UNIQUE,
  descripcion_corta NVARCHAR(MAX),
  preparacion NVARCHAR(MAX),
  tiempo_min INT,
  porciones INT,
  precio DECIMAL(6,2),
  imagen_url VARCHAR(255),
  categoria_id INT,
  fecha_publicacion DATE,
  FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);
GO

CREATE TABLE ingrediente (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  unidad_base VARCHAR(20),
  descripcion NVARCHAR(MAX)
);
GO

CREATE TABLE etiqueta (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(50) NOT NULL UNIQUE
);
GO

CREATE TABLE reposteria (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  slug VARCHAR(100) NOT NULL UNIQUE,
  descripcion NVARCHAR(MAX),
  precio DECIMAL(6,2)
);
GO

CREATE TABLE utensilio (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  slug VARCHAR(100) NOT NULL UNIQUE,
  descripcion NVARCHAR(MAX)
);
GO

CREATE TABLE nutricion (
  batido_id INT PRIMARY KEY,
  kcal INT,
  proteina_g DECIMAL(6,2),
  grasa_g DECIMAL(6,2),
  carbo_g DECIMAL(6,2),
  azucar_g DECIMAL(6,2),
  fibra_g DECIMAL(6,2),
  sodio_mg DECIMAL(6,2),
  FOREIGN KEY (batido_id) REFERENCES batido(id)
);
GO

CREATE TABLE batido_ingrediente (
  batido_id INT,
  ingrediente_id INT,
  cantidad DECIMAL(6,2),
  unidad VARCHAR(20),
  PRIMARY KEY (batido_id, ingrediente_id),
  FOREIGN KEY (batido_id) REFERENCES batido(id),
  FOREIGN KEY (ingrediente_id) REFERENCES ingrediente(id)
);
GO

CREATE TABLE batido_etiqueta (
  batido_id INT,
  etiqueta_id INT,
  PRIMARY KEY (batido_id, etiqueta_id),
  FOREIGN KEY (batido_id) REFERENCES batido(id),
  FOREIGN KEY (etiqueta_id) REFERENCES etiqueta(id)
);
GO

CREATE TABLE batido_reposteria (
  batido_id INT,
  reposteria_id INT,
  cantidad INT,
  PRIMARY KEY (batido_id, reposteria_id),
  FOREIGN KEY (batido_id) REFERENCES batido(id),
  FOREIGN KEY (reposteria_id) REFERENCES reposteria(id)
);
GO

CREATE TABLE batido_utensilio (
  batido_id INT,
  utensilio_id INT,
  cantidad INT,
  PRIMARY KEY (batido_id, utensilio_id),
  FOREIGN KEY (batido_id) REFERENCES batido(id),
  FOREIGN KEY (utensilio_id) REFERENCES utensilio(id)
);
GO
