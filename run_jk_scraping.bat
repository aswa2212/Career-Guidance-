@echo off
echo ========================================
echo   REAL Web Scraping from Internet
echo ========================================
echo.
echo This will scrape REAL data from:
echo - J&K Government Education Websites
echo - Educational Aptitude Question Sites
echo - University and College Portals
echo - Online Learning Platforms
echo.

cd /d "career-tracking-backend"

echo Installing scraping dependencies...
pip install -r scraping_requirements.txt

echo.
echo Starting REAL web scraping from internet...
echo This will take 10-20 minutes depending on internet speed.
echo.

python scrape_real_data.py

echo.
echo ========================================
echo    REAL Web Scraping Complete
echo ========================================
echo.
echo Check the following:
echo - real_scraping.log (detailed logs)
echo - real_scraped_data/ folder (JSON backups)
echo - real_ml_aptitude_dataset_*.json (ML training data)
echo.
echo Your database now contains REAL data from internet:
echo - J&K Government Colleges (from gov websites)
echo - Aptitude Questions (from educational sites)
echo - Course and Career Data
echo.

pause
