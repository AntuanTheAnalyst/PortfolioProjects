/*

Cleaning Data in PostgreSQL Queries

*/

--------------------------------------------------------------------------------------------------------------------------

-- Converting columns to appropriate data types

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


-- Standardize Date Format

ALTER TABLE nashvillehousing
ALTER COLUMN SaleDate TYPE DATE USING TO_DATE(SaleDate, 'Month DD, YYYY');

 --------------------------------------------------------------------------------------------------------------------------

-- Populating Property Address data

SELECT a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, COALESCE(a.PropertyAddress, b.PropertyAddress)
FROM PortfolioProject.dbo.NashvilleHousing AS a
INNER JOIN PortfolioProject.dbo.NashvilleHousing AS b
	ON a.ParcelID = b.ParcelID
	AND a.uniqueid != b.uniqueid
WHERE a.PropertyAddress IS NULL


UPDATE nashvillehousing AS a
SET PropertyAddress = COALESCE(a.PropertyAddress, b.PropertyAddress)
FROM nashvillehousing AS b
WHERE a.parcelid = b.parcelid
	AND a.parcelid != b.parcelid
	AND a.propertyaddress IS NULL;

--------------------------------------------------------------------------------------------------------------------------

-- Breaking out Address into Individual Columns (Address, City, State)

SELECT PropertyAddress
FROM nashvillehousing
--Where PropertyAddress is null
--order by ParcelID

SELECT
SUBSTRING(PropertyAddress, 1, POSITION(',' IN PropertyAddress) -1 ) AS Address,
SUBSTRING(PropertyAddress, POSITION(',' IN PropertyAddress) + 1 , LENGTH(PropertyAddress)) AS Address
--or STRPOS(propertyaddress, ',')
FROM nashvillehousing


ALTER TABLE nashvillehousing
ADD PropertySplitAddress VARCHAR(255);

UPDATE nashvillehousing
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, POSITION(',' IN PropertyAddress) -1 )


ALTER TABLE nashvillehousing
ADD PropertySplitCity Nvarchar(255);

Update nashvillehousing
SET PropertySplitCity = SUBSTRING(PropertyAddress, POSITION(',' IN PropertyAddress) + 1 , LENGTH(PropertyAddress))


SELECT *
FROM nashvillehousing


-- Second way of doing that. Easier

SELECT OwnerAddress
FROM nashvillehousing


SELECT 
    split_part(address, ',', 1) AS part1, 
    split_part(address, ',', 2) AS part2, 
    split_part(address, ',', 3) AS part3  
FROM nashvillehousing;

-- Step 1: Adding new columns

ALTER TABLE nashvillehousing
ADD COLUMN OwnerAddress TEXT,
ADD COLUMN OwnerCity TEXT,
ADD COLUMN OwnerState TEXT;

-- Step 2: Populating new columns by splitting the address

UPDATE nashvillehousing
SET 
    OwnerAddress = trim(split_part(address, ',', 1)),
    OwnerCity = trim(split_part(address, ',', 2)),
    OwnerState = trim(split_part(address, ',', 3));

SELECT address, OwnerAddress, OwnerCity, OwnerState
FROM nashvillehousing;


--------------------------------------------------------------------------------------------------------------------------


-- Change Y and N to Yes and No in "Sold as Vacant" field


SELECT DISTINCT SoldAsVacant, COUNT(SoldAsVacant)
From nashvillehousing
GROUP BY SoldAsVacant
ORDER BY 2



Select SoldAsVacant
, CASE When SoldAsVacant = 'Y' THEN 'Yes'
	   When SoldAsVacant = 'N' THEN 'No'
	   ELSE SoldAsVacant
	   END
From nashvillehousing


Update nashvillehousing
SET SoldAsVacant = CASE When SoldAsVacant = 'Y' THEN 'Yes'
	   When SoldAsVacant = 'N' THEN 'No'
	   ELSE SoldAsVacant
	   END
	   

-----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Remove Duplicates

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
--order by ParcelID
)
SELECT *
FROM RowNumCTE
WHERE row_num > 1
ORDER BY PropertyAddress


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

Select *
From nashvillehousing


ALTER TABLE nashvillehousing
DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress, SaleDate

