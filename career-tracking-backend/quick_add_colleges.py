#!/usr/bin/env python3
"""
Quick script to add sample college data to the database
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.college import College

# Database URL
DATABASE_URL = "postgresql+asyncpg://postgres:Postgresql%400001@localhost/career_db"

# Sample college data
SAMPLE_COLLEGES = [
    {
        "name": "Indian Institute of Technology Delhi",
        "address": "Hauz Khas, New Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110016",
        "website": "https://home.iitd.ac.in/",
        "latitude": 28.5449,
        "longitude": 77.1928,
        "scholarship_details": "Merit-based scholarships available"
    },
    {
        "name": "Indian Institute of Technology Bombay",
        "address": "Powai, Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400076",
        "website": "https://www.iitb.ac.in/",
        "latitude": 19.1334,
        "longitude": 72.9133,
        "scholarship_details": "Need-based and merit scholarships"
    },
    {
        "name": "Delhi University",
        "address": "University Enclave, Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110007",
        "website": "https://www.du.ac.in/",
        "latitude": 28.6862,
        "longitude": 77.2090,
        "scholarship_details": "Various government scholarships available"
    },
    {
        "name": "Jawaharlal Nehru University",
        "address": "New Mehrauli Road, New Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110067",
        "website": "https://www.jnu.ac.in/",
        "latitude": 28.5383,
        "longitude": 77.1641,
        "scholarship_details": "UGC scholarships and fellowships"
    },
    {
        "name": "Anna University",
        "address": "Sardar Patel Road, Guindy",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600025",
        "website": "https://www.annauniv.edu/",
        "latitude": 13.0067,
        "longitude": 80.2206,
        "scholarship_details": "State government scholarships available"
    }
]

async def add_colleges():
    """Add sample colleges to the database"""
    try:
        # Create async engine
        engine = create_async_engine(DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Check if colleges already exist
            from sqlalchemy import select
            result = await session.execute(select(College))
            existing_colleges = result.scalars().all()
            
            if existing_colleges:
                print(f"Found {len(existing_colleges)} existing colleges. Skipping insertion.")
                return
            
            # Add sample colleges
            for college_data in SAMPLE_COLLEGES:
                college = College(**college_data)
                session.add(college)
            
            await session.commit()
            print(f"Successfully added {len(SAMPLE_COLLEGES)} colleges to the database!")
            
    except Exception as e:
        print(f"Error adding colleges: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(add_colleges())
