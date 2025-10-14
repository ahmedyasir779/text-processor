from info_extractor import InfoExtractor

# Sample resume text
resume_text = """
AHMED AL-HASSAN
Software Engineer

Contact:
Email: ahmed.hassan@email.com
Phone: +966-50-123-4567
LinkedIn: https://linkedin.com/in/ahmed-hassan
GitHub: https://github.com/ahmed-hassan

EXPERIENCE:

Senior Developer at TechCorp (2020-01-15 to present)
- Led team of 5 developers
- Increased performance by 40%
- Salary: SAR 180,000 per year

SKILLS:
#Python #MachineLearning #Docker #AWS
Follow my work: @ahmed_dev

References available upon request.
Meeting availability: Monday-Friday, 9:00 AM to 5:00 PM
"""

print("=" * 60)
print("EXTRACTING INFORMATION FROM RESUME")
print("=" * 60)

extractor = InfoExtractor(resume_text)

print("\n Contact Email: ")
email = extractor.extract_emails()
print(f" {email[0] if email else 'Not found'}")

print("\n Phone: ")
phone = extractor.extract_phones()
print(f" {phone[0] if phone else 'Not found'}")

print("\n Social Media: ")
urls = extractor.extract_urls()
for url in urls:
    print(f"  - {url}")

print("\n Salary: ")
salary = extractor.extract_currency()
print(f" {salary[0] if salary else 'Not specified'}")

print("\n Skills (hashtags) : ")
skills = extractor.extract_hashtags()
for skill in skills:
    print(f"  - {skill}")

print("\n Employment Dates: ")
dates = extractor.extract_dates()
for date in dates:
    print(f"  - {date}")

print("\n Avaliability: ")
times = extractor.extract_times()
for time in times:
    print(f"  - {time}")

print("\n " + "=" * 60)
print("Extraction Complete!")
print("=" * 60)

