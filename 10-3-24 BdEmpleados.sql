CREATE DATABASE [TareaP1]
GO;

USE [TareaP1]
GO;

CREATE TABLE dbo.Empleado
(
id INT IDENTITY (1, 1) PRIMARY KEY
, Nombre VARCHAR(128) NOT NULL
, Salario MONEY NOT NULL
 )
 GO;

 -- Inserción de empleados
 INSERT INTO [dbo].[Empleado] (Empleado.[Nombre], Empleado.[Salario]) 
 VALUES 
('Fernando Sanchez', 100),
('Agnes Martinez', 96099),
('Irena Mcginty', 25363),
('James Lee', 26421),
('Ryan Abbott', 13094),
('David Garcia', 92869),
('Douglas Apadoca', 67628),
('Lisa Reed', 62308),
('Erich Hernandez', 89000),
('Tammy Mcdonald', 49858),
('William Chadwell', 58334),
('Joseph Carroll', 55553),
('Flor Micale', 33533),
('Jeremy Maciel', 35336),
('Douglas Byrd', 45208),
('Thomas Fenster', 1226),
('Susan Grier', 3308),
('James Johnson', 80181),
('Nathan Vann', 13866),
('Jeffrey Brunson', 45736),
('Pam Newman', 77566),
('Timothy Thomas', 22363),
('Norman Kantrowitz', 14781),
('Robert Schrock', 69451),
('Theresa Comley', 67669),
('Jose Hamons', 97210),
('Barbara Rome', 2096),
('Phillip Leach', 66390),
('Leonor Angulo', 24147),
('Mark Grant', 35203),
('Ricardo Thurman', 8300),
('William Acevedo', 74264),
('Margret Hobbs', 18371),
('Garry Miller', 16078),
('Peter Martir', 86497),
('Paul Johnston', 55991),
('Malia Huguley', 85415),
('Troy Wallace', 29628),
('Richard Ellis', 21032),
('Pearl Morse', 35274),
('Manuel Mcnair', 63245)
GO;

-- SP para listar empleados
CREATE PROCEDURE [dbo].[ListarEmpleados]
AS
BEGIN
	BEGIN TRY
		SET NOCOUNT ON;
		SELECT 
			[id],
			[Nombre],
			[Salario]
		FROM [TareaP1].[dbo].[Empleado]
		ORDER BY 2
		SET NOCOUNT OFF;
	END TRY
	BEGIN CATCH
		SELECT 'Error'
	END CATCH
END

-- Ejecutar SP ListarEmpleados
EXEC ListarEmpleados
GO;

-- SP para insertar un empleado
CREATE PROCEDURE [dbo].[InsertarEmpleado]
	@inNombre VARCHAR(128),
	@inSalario MONEY,
	@outResultCode INT OUTPUT
AS
BEGIN
	SET @outResultCode = 0
	BEGIN TRAN
	BEGIN TRY
		SET NOCOUNT ON;
		INSERT INTO [dbo].[Empleado] ([Nombre], [Salario]) VALUES (@inNombre, @inSalario)

		IF (SELECT COUNT([Nombre]) --verifica si hay repetidos luego de insertar un nombre
			FROM [dbo].[Empleado]
			GROUP BY [Nombre]
			HAVING COUNT([Nombre]) > 1) > 1
			BEGIN
				SET @outResultCode = 50001
				ROLLBACK
			END
		ELSE
		BEGIN
			COMMIT
		END
		SET NOCOUNT OFF;
	END TRY
	BEGIN CATCH
		SET @outResultCode = 50002
		ROLLBACK
	END CATCH
END
GO;

SET NOCOUNT ON;
DECLARE @out INT;
EXEC [dbo].[InsertarEmpleado] @inNombre = 'a', @inSalario = 0.3, @outResultCode = @out OUTPUT;
SELECT @out AS the_output;

CREATE ROLE SpExec
GRANT EXEC TO SpExec