#!/usr/bin/env python3
"""
Delhi Job Search Agent
Finds and categorizes jobs in Delhi by job type
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from fake_useragent import UserAgent
import time


class JobAgent:
    """Agent to search and categorize jobs in Delhi"""
    
    JOB_TYPES = {
        'full-time': ['full time', 'full-time', 'fulltime', 'permanent', 'regular'],
        'part-time': ['part time', 'part-time', 'parttime'],
        'contract': ['contract', 'contractual', 'temporary', 'temp'],
        'internship': ['intern', 'internship', 'trainee'],
        'freelance': ['freelance', 'freelancer', 'consultant'],
        'remote': ['remote', 'work from home', 'wfh', 'telecommute']
    }
    
    def __init__(self):
        self.ua = UserAgent()
        self.jobs = []
        self.session = requests.Session()
        
    def get_headers(self) -> Dict[str, str]:
        """Generate random user agent headers"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def categorize_job_type(self, title: str, description: str) -> str:
        """Categorize job based on title and description"""
        text = f"{title} {description}".lower()
        
        for job_type, keywords in self.JOB_TYPES.items():
            for keyword in keywords:
                if keyword in text:
                    return job_type
        
        return 'full-time'  # Default
    
    def scrape_timesjobs(self, max_pages: int = 3) -> List[Dict]:
        """Scrape jobs from TimesJobs"""
        jobs = []
        base_url = "https://www.timesjobs.com/candidate/job-search.html"
        
        print("🔍 Searching TimesJobs...")
        
        for page in range(1, max_pages + 1):
            try:
                params = {
                    'searchType': 'personalizedSearch',
                    'from': 'submit',
                    'txtKeywords': '',
                    'txtLocation': 'Delhi',
                    'sequence': page
                }
                
                response = self.session.get(
                    base_url,
                    params=params,
                    headers=self.get_headers(),
                    timeout=10
                )
                
                if response.status_code != 200:
                    print(f"  ⚠️  Page {page}: Status {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'lxml')
                job_listings = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
                
                for job in job_listings:
                    try:
                        title_tag = job.find('h2')
                        title = title_tag.text.strip() if title_tag else 'N/A'
                        
                        company_tag = job.find('h3', class_='joblist-comp-name')
                        company = company_tag.text.strip() if company_tag else 'N/A'
                        
                        exp_tag = job.find('ul', class_='top-jd-dtl clearfix')
                        experience = 'N/A'
                        if exp_tag:
                            exp_li = exp_tag.find('li')
                            if exp_li:
                                experience = exp_li.text.strip()
                        
                        desc_tag = job.find('ul', class_='list-job-dtl clearfix')
                        description = desc_tag.text.strip() if desc_tag else ''
                        
                        skills_tag = job.find('span', class_='srp-skills')
                        skills = skills_tag.text.strip() if skills_tag else 'N/A'
                        
                        job_type = self.categorize_job_type(title, description)
                        
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': 'Delhi',
                            'experience': experience,
                            'skills': skills,
                            'job_type': job_type,
                            'description': description[:200],
                            'source': 'TimesJobs',
                            'scraped_at': datetime.now().isoformat()
                        })
                    except Exception as e:
                        continue
                
                print(f"  ✓ Page {page}: Found {len(job_listings)} listings")
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"  ✗ Page {page}: Error - {str(e)}")
                continue
        
        return jobs
    
    def scrape_naukri_style(self) -> List[Dict]:
        """Generate sample jobs in Naukri.com style (for demonstration)"""
        print("🔍 Generating sample job data...")
        
        sample_jobs = [
            {
                'title': 'Senior Software Engineer',
                'company': 'Tech Solutions India',
                'location': 'Delhi NCR',
                'experience': '3-5 years',
                'skills': 'Python, Django, REST API, PostgreSQL',
                'job_type': 'full-time',
                'description': 'Looking for experienced software engineer to work on enterprise applications',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Data Analyst Intern',
                'company': 'Analytics Corp',
                'location': 'Delhi',
                'experience': '0-1 years',
                'skills': 'Python, Pandas, SQL, Excel, Power BI',
                'job_type': 'internship',
                'description': 'Internship opportunity for data analysis and visualization projects',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Freelance Content Writer',
                'company': 'Digital Marketing Agency',
                'location': 'Delhi (Remote)',
                'experience': '1-3 years',
                'skills': 'Content Writing, SEO, Blog Writing',
                'job_type': 'freelance',
                'description': 'Freelance content writers needed for various digital marketing projects',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Part-Time Sales Associate',
                'company': 'Retail Solutions',
                'location': 'Connaught Place, Delhi',
                'experience': '0-2 years',
                'skills': 'Customer Service, Sales, Communication',
                'job_type': 'part-time',
                'description': 'Part-time sales position for weekend shifts',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Contract Java Developer',
                'company': 'IT Services Ltd',
                'location': 'Gurgaon/Delhi NCR',
                'experience': '4-6 years',
                'skills': 'Java, Spring Boot, Microservices, AWS',
                'job_type': 'contract',
                'description': '6-month contract position for Java development on cloud-based projects',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Remote Digital Marketing Manager',
                'company': 'E-commerce Startup',
                'location': 'Delhi (Work From Home)',
                'experience': '2-4 years',
                'skills': 'Digital Marketing, SEO, SEM, Social Media',
                'job_type': 'remote',
                'description': 'Remote position for managing digital marketing campaigns',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Full Stack Developer',
                'company': 'Innovative Tech',
                'location': 'Delhi',
                'experience': '2-5 years',
                'skills': 'React, Node.js, MongoDB, Express',
                'job_type': 'full-time',
                'description': 'Full-time position for MERN stack development',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Business Analyst Trainee',
                'company': 'Consulting Firm',
                'location': 'Delhi NCR',
                'experience': '0-1 years',
                'skills': 'Business Analysis, Excel, SQL, Communication',
                'job_type': 'internship',
                'description': 'Trainee program for aspiring business analysts',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Graphic Designer (Freelance)',
                'company': 'Creative Agency',
                'location': 'Delhi',
                'experience': '1-3 years',
                'skills': 'Adobe Photoshop, Illustrator, UI/UX Design',
                'job_type': 'freelance',
                'description': 'Project-based freelance work for graphic design',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'HR Manager',
                'company': 'Manufacturing Company',
                'location': 'Delhi',
                'experience': '5-8 years',
                'skills': 'HR Management, Recruitment, Employee Relations',
                'job_type': 'full-time',
                'description': 'Permanent position for HR management and operations',
                'source': 'Sample Data',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        return sample_jobs
    
    def search_jobs(self, use_live_scraping: bool = False) -> List[Dict]:
        """Main method to search for jobs"""
        print("\n" + "="*60)
        print("🤖 DELHI JOB SEARCH AGENT")
        print("="*60 + "\n")
        
        all_jobs = []
        
        if use_live_scraping:
            # Try live scraping (may not work due to anti-scraping measures)
            timesjobs_data = self.scrape_timesjobs(max_pages=2)
            all_jobs.extend(timesjobs_data)
        
        # Always include sample data for demonstration
        sample_data = self.scrape_naukri_style()
        all_jobs.extend(sample_data)
        
        self.jobs = all_jobs
        return all_jobs
    
    def analyze_jobs(self) -> Dict:
        """Analyze collected jobs and generate statistics"""
        if not self.jobs:
            return {}
        
        df = pd.DataFrame(self.jobs)
        
        analysis = {
            'total_jobs': len(self.jobs),
            'by_job_type': df['job_type'].value_counts().to_dict(),
            'by_company': df['company'].value_counts().head(10).to_dict(),
            'by_source': df['source'].value_counts().to_dict(),
            'unique_companies': df['company'].nunique(),
        }
        
        return analysis
    
    def save_results(self, filename_prefix: str = 'delhi_jobs'):
        """Save results to CSV and JSON files"""
        if not self.jobs:
            print("⚠️  No jobs to save")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save to CSV
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        df = pd.DataFrame(self.jobs)
        df.to_csv(csv_filename, index=False)
        print(f"✓ Saved to CSV: {csv_filename}")
        
        # Save to JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved to JSON: {json_filename}")
        
        # Save analysis
        analysis = self.analyze_jobs()
        analysis_filename = f"{filename_prefix}_analysis_{timestamp}.json"
        with open(analysis_filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved analysis: {analysis_filename}")
    
    def display_results(self):
        """Display job search results"""
        if not self.jobs:
            print("⚠️  No jobs found")
            return
        
        print(f"\n📊 RESULTS SUMMARY")
        print("="*60)
        print(f"Total Jobs Found: {len(self.jobs)}")
        
        # Group by job type
        df = pd.DataFrame(self.jobs)
        print(f"\n📋 Jobs by Type:")
        job_type_counts = df['job_type'].value_counts()
        for job_type, count in job_type_counts.items():
            print(f"  • {job_type.title()}: {count}")
        
        print(f"\n🏢 Top Companies:")
        company_counts = df['company'].value_counts().head(5)
        for company, count in company_counts.items():
            print(f"  • {company}: {count} positions")
        
        print(f"\n💼 Sample Jobs:")
        print("-"*60)
        for i, job in enumerate(self.jobs[:5], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Type: {job['job_type'].upper()}")
            print(f"   Experience: {job['experience']}")
            print(f"   Skills: {job['skills']}")
        
        if len(self.jobs) > 5:
            print(f"\n... and {len(self.jobs) - 5} more jobs")
        
        print("\n" + "="*60)


def main():
    """Main execution function"""
    agent = JobAgent()
    
    # Search for jobs (set use_live_scraping=True to attempt live scraping)
    jobs = agent.search_jobs(use_live_scraping=False)
    
    # Display results
    agent.display_results()
    
    # Save results
    print("\n💾 Saving results...")
    agent.save_results()
    
    print("\n✅ Job search completed successfully!")
    print("\nℹ️  Note: This demo uses sample data. For live scraping,")
    print("   set use_live_scraping=True in the search_jobs() method.")


if __name__ == "__main__":
    main()
