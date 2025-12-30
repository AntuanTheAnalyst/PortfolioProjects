/*
Covid 19 Data Exploration with PostgreSQL

Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types

*/

SELECT * FROM coviddeaths
WHERE continent IS NOT NULL
ORDER BY 3, 4


-- Select Data that we are going to be starting with

SELECT location, date, total_cases, new_cases, total_deaths, population FROM coviddeaths
WHERE continent IS NOT NULL 
ORDER BY 1,2


-- Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in your country

SELECT Location, date, total_cases,total_deaths, (total_deaths/total_cases)*100 AS DeathPercentage
FROM coviddeaths
WHERE LOCATION = 'Turkey'
AND continent IS NOT NULL
ORDER BY 1, 2 


-- Total Cases vs Population
-- Shows what percentage of population infected with Covid

SELECT Location, date, Population, total_cases,  (total_cases/population)*100 AS PercentPopulationInfected
FROM coviddeaths
--Where location like '%states%'
ORDERY BY 1, 2


-- Countries with Highest Infection Rate compared to Population

SELECT location, population, MAX(total_cases) as HighestInfectionCount,  MAX((total_cases/population))*100 as PercentPopulationInfected
From coviddeaths
--Where location like '%states%'
GROUP BY location, population
ORDER BY PercentPopulationInfected DESC


-- Countries with Highest Death Count per Population

SELECT location, MAX(CAST(Total_deaths as int)) as TotalDeathCount
From coviddeaths
--Where location like '%states%'
WHERE continent IS NOT NULL
GROUP BY Location
ORDER BY TotalDeathCount desc


-- BREAKING THINGS DOWN BY CONTINENT

-- Showing contintents with the highest death count per population

SELECT continent, MAX(total_deaths) as TotalDeathCount 
FROM coviddeaths
WHERE continent IS NOT NULL
GROUP BY continent
-- WHERE location ILIKE '%turkey'
ORDER BY TotalDeathCount DESC


-- GLOBAL NUMBERS

SELECT SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/SUM(new_cases) * 100 as DeathPercentage 
FROM coviddeaths
WHERE continent IS NOT NULL
-- GROUP BY date
ORDER BY 1, 2


-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM coviddeaths dea
INNER JOIN covidvaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL 
ORDER BY 2,3


-- Using CTE to perform Calculation on Partition By in previous query

With PopvsVac (continent, location, date, population, new_vaccinations, rolling_people_vaccinated)
AS
(
	SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) 
	AS rolling_people_vaccinated 
	-- (rolling_people_vaccinated / population) * 100 
	FROM coviddeaths dea
	INNER JOIN covidvaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
	WHERE dea.continent is not null
	-- ORDER BY 2, 3
)
SELECT *, (rolling_people_vaccinated/population) * 100 FROM PopvsVAc


-- Using Temp Table to perform Calculation on Partition By in previous query

DROP TABLE IF EXISTS PercentPopulationVaccinated
CREATE TABLE PercentPopulationVaccinated
(
	continent VARCHAR(255),
	location VARCHAR(255),
	date DATE,
	population NUMERIC,
	new_vaccinations NUMERIC,
	rolling_people_vaccinated NUMERIC		
)

INSERT INTO PercentPopulationVaccinated
	SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) 
	AS rolling_people_vaccinated 
	-- (rolling_people_vaccinated / population) * 100 
	FROM coviddeaths dea
	INNER JOIN covidvaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
	WHERE dea.continent is not null
	ORDER BY 2, 3

SELECT *, (rolling_people_vaccinated/population) * 100 FROM PercentPopulationVaccinated


-- Creating View to Store Data For later visualizations

CREATE VIEW PercentPopulationVaccinated2 AS
	SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) 
	AS rolling_people_vaccinated 
	-- (rolling_people_vaccinated / population) * 100 
	FROM coviddeaths dea
	INNER JOIN covidvaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
	WHERE dea.continent IS NOT NULL
	



