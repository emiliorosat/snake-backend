-- SQLite
CREATE TABLE if NOT EXISTS [Paciente] (
[Id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[UsuarioId] INTEGER  NULL,
[Cedula] VARCHAR(15)  NULL,
[Foto] VARCHAR(200)  NULL,
[Nombre] VARCHAR(50)  NULL,
[Apellido] VARCHAR(50)  NULL,
[TipoSangre] vaRCHAR(5)  NULL,
[Email] varCHAR(50)  NULL,
[Sexo] VARCHAR(1)  NULL,
[FechaNacimiento] DATE  NULL,
[AlergiasId] INTEGER  NULL,
[SignoZodiacal] VARCHAR(20)  NULL
);

CREATE TABLE if NOT EXISTS [Consulta] (
[PacienteId] INTEGER  NULL,
[Fecha] DATE  NULL,
[Motivo] TEXT  NULL,
[Seguro] VARCHAR(100)  NULL,
[MontoPagado] FLOAT  NULL,
[Diagnostico] TEXT  NULL,
[Notas] TEXT  NULL,
[Archivo] VARCHAR(200)  NULL
);

CREATE TABLE if NOT EXISTS  [Alergia] (
[Id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[Nombre] VARCHAR(100)  NULL
);

