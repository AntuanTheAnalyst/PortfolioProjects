/*

Cleaning Data in PostgreSQL Queries

*/

--------------------------------------------------------------------------------------------------------------------------

-- Converting columns to appropriate data types
-- Using NULLIF to handle empty strings

ALTER TABLE nashvillehousing
ALTER COLUMN SalePrice TYPE FLOAT USING NULLIF(SalePrice, '')::FLOAT,
ALTER COLUMN Acreage TYPE FLOAT USING NULLIF(Acreage, '')::FLOAT,
ALTER COLUMN LandValue TYPE FLOAT USING NULLIF(LandValue, '')::FLOAT,
ALTER COLUMN BuildingValue TYPE FLOAT USING NULLIF(BuildingValue, '')::FLOAT,
ALTER COLUMN TotalValue TYPE FLOAT USING NULLIF(TotalValue, '')::FLOAT,
ALTER COLUMN YearBuilt TYPE INTEGER USING NULLIF(YearBuilt, '')::INTEGER,
ALTER COLUMN Bedrooms TYPE INTEGER USING NULLIF(Bedrooms, '')::INTEGER,
ALTER COLUMN FullBath TYPE INTEGER USING NULLIF(FullBath, '')::INTEGER,
ALTER COLUMN HalfBath TYPE INTEGER USING NULLIF(HalfBath, '')::INTEGER;


-- Standardizing the date Format

ALTER TABLE nashvillehousing
ALTER COLUMN SaleDate TYPE DATE USING TO_DATE(SaleDate, 'Month DD, YYYY');

 --------------------------------------------------------------------------------------------------------------------------

-- Populating Property Address data

SELECT a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, COALESCE(a.PropertyAddress, b.PropertyAddress)
FROM nashvillehousing AS a
INNER JOIN nashvillehousing AS b
	ON a.ParcelID = b.ParcelID
	AND a.uniqueid != b.uniqueid
WHERE a.PropertyAddress IS NULL


UPDATE nashvillehousing AS a
SET PropertyAddress = COALESCE(a.PropertyAddress, b.PropertyAddress)
FROM nashvillehousing AS b
WHERE a.parcelID = b.parcelID
	AND a.uniqueid != b.uniqueid
	AND a.propertyaddress IS NULL;

--------------------------------------------------------------------------------------------------------------------------

-- Breaking out Address into Individual Columns (Address, City, State)

SELECT PropertyAddress
FROM nashvillehousing
--Where PropertyAddress is null
--order by ParcelID

SELECT 
    SUBSTRING(PropertyAddress, 1, POSITION(',' IN PropertyAddress) - 1) AS Address,
    SUBSTRING(PropertyAddress, POSITION(',' IN PropertyAddress) + 1, LENGTH(PropertyAddress)) AS CityState
FROM nashvillehousing;

-- Adding new columns for split address components.
ALTER TABLE nashvillehousing
ADD COLUMN PropertySplitAddress VARCHAR(255),
ADD COLUMN PropertySplitCity VARCHAR(255),
ADD COLUMN PropertySplitState VARCHAR(255);

-- Populating the new columns with split values.
UPDATE nashvillehousing
SET PropertySplitAddress = TRIM(SPLIT_PART(PropertyAddress, ',', 1)),
    PropertySplitCity = TRIM(SPLIT_PART(PropertyAddress, ',', 2)),
    PropertySplitState = TRIM(SPLIT_PART(PropertyAddress, ',', 3));

--------------------------------------------------------------------------------------------------------------------------


-- Changing "Y" and "N" to "Yes" and "No" in "SoldasVacant" field


SELECT DISTINCT SoldAsVacant, COUNT(SoldAsVacant)
FROM nashvillehousing
GROUP BY SoldAsVacant
ORDER BY 2


-- Updating values to "Yes" and "No".

UPDATE nashvillehousing
SET SoldAsVacant = CASE 
	   WHEN SoldAsVacant = 'Y' THEN 'Yes'
	   WHEN SoldAsVacant = 'N' THEN 'No'
	   ELSE SoldAsVacant
	   END
	   

-----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Removing Duplicates
-- Using a CTE to identify duplicate rows based on specific columns 
-- and retaining only the first occurrence.

WITH RowNumCTE AS(
SELECT *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY
					UniqueID
					) AS row_num

FROM nashvillehousing

--Reviewing Duplicate rows
)
SELECT *
FROM RowNumCTE
WHERE row_num > 1
ORDER BY PropertyAddress

-- Deleting duplicates based on the generated row numbers.
DELETE FROM nashvillehousing
WHERE uniqueid IN (
    SELECT uniqueid
    FROM (
        SELECT uniqueid, 
               ROW_NUMBER() OVER (
                   PARTITION BY parcelid, propertyaddress, saleprice, saledate, legalreference
                   ORDER BY uniqueid
               ) AS row_num
        FROM nashvillehousing
    ) subquery
    WHERE row_num > 1
);

SELECT *
FROM nashvillehousing


---------------------------------------------------------------------------------------------------------

-- Deleting Unused Columns
-- Removing columns that are no longer needed after the cleaning process.

SELECT *
FROM nashvillehousing


ALTER TABLE nashvillehousing
DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress, SaleDate



