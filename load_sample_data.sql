-- Load sample VCAT evidence data into mygpt-vcat-db
-- This creates representative evidence entries for testing

-- Insert sample documents
INSERT INTO evidence.documents (filename, file_path, file_type, file_hash, file_size, title, content, document_date, created_at) VALUES
('20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.html', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.html', 'html', '5f4d2e33c28a8e6b2c8e9c1f7a3b4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', 15420, 'Urgent Water Damage Report', 'Water damage on bedroom wall Unit 1803 243 Franklin Street Melbourne urgent repair required damage spreading mold risk tenant safety concern property management response needed', '2025-04-16', NOW()),

('20250624-RDRV - Case RT252398 - 33 Camberwell Rd, Hawthorn -57.html', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/20250624-RDRV - Case RT252398 - 33 Camberwell Rd, Hawthorn -57.html', 'html', 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 12890, 'VCAT Case RT252398', 'RDRV residential tenancy dispute resolution Victoria case RT252398 Camberwell Road Hawthorn property management tenant rights dispute VCAT hearing scheduled', '2025-06-24', NOW()),

('20250714-VCAT Application R202518214_00 – Challenge to Noti-5.html', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/20250714-VCAT Application R202518214_00 – Challenge to Noti-5.html', 'html', 'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3', 18760, 'VCAT Notice Challenge Application', 'VCAT application R202518214 challenge notice to vacate tenant rights residential tenancy dispute Victoria civil administrative tribunal hearing', '2025-07-14', NOW()),

('27-06-2025 - Strike out - Consent order - Order f058873a.pdf', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/Attachments-13/27-06-2025 - Strike out - Consent order - Order f058873a.pdf', 'pdf', 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4', 156000, 'VCAT Strike Out Consent Order', 'VCAT consent order strike out application resolved parties agreement settlement terms conditions Victorian Civil Administrative Tribunal', '2025-06-27', NOW()),

('Receipt # 91716.pdf', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/Attachments/Receipt # 91716.pdf', 'pdf', 'd4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5', 89450, 'Payment Receipt 91716', 'rent payment receipt 2100 dollars 1803 243 Franklin Street Melbourne monthly rental payment property management Areal Property', '2025-02-25', NOW());

-- Insert sample emails
INSERT INTO evidence.emails (filename, file_path, file_hash, file_size, subject, sender, recipient, email_date, body_text, created_at) VALUES
('20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.eml', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_EML/20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.eml', 'e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 8940, 'Urgent: Water Damage on Bedroom Wall (Unit 1803)', 'chawakorn@example.com', 'property@arealproperty.com.au', '2025-04-16 08:30:00', 'Dear Property Manager, I am writing to report urgent water damage in my bedroom wall at Unit 1803, 243 Franklin Street, Melbourne. Water is seeping through the wall causing damage to paint and potentially structural issues. This requires immediate attention as the damage appears to be spreading. Please arrange for urgent inspection and repair. The damage is affecting my ability to use the bedroom safely. Photos attached showing extent of damage. Urgent response needed. Thank you, Chawakorn', NOW()),

('20250624-RDRV - Case RT252398 - 33 Camberwell Rd, Hawthorn -57.eml', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_EML/20250624-RDRV - Case RT252398 - 33 Camberwell Rd, Hawthorn -57.eml', 'f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7', 15670, 'RDRV - Case RT252398 - 33 Camberwell Rd, Hawthorn', 'rdrv@vcat.vic.gov.au', 'chawakorn@example.com', '2025-06-24 14:20:00', 'Dear Mr Kamnuansil, VCAT has received your residential tenancy dispute application RT252398 regarding the property at 33 Camberwell Road, Hawthorn. Your application has been registered and a case number assigned. The dispute resolution process will commence with an attempt at conciliation. If conciliation is unsuccessful, the matter will proceed to hearing. All parties will be notified of hearing dates and requirements. Please ensure you have all necessary documentation ready for the proceedings. VCAT Registry', NOW()),

('20250225-Receipt of payment for 1803_243 Franklin St, Melbo-110.eml', 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_EML/20250225-Receipt of payment for 1803_243 Franklin St, Melbo-110.eml', 'a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8', 7230, 'Receipt of payment for 1803/243 Franklin St, Melbourne', 'accounts@arealproperty.com.au', 'chawakorn@example.com', '2025-02-25 10:15:00', 'Dear Chawakorn, Thank you for your rental payment. Property: 1803/243 Franklin Street, Melbourne. Amount: $2,100.00. Payment Date: 25 February 2025. Receipt Number: #91716. Payment Method: Bank Transfer. Next payment due: 25 March 2025. If you have any queries regarding this payment or your tenancy, please contact our office. Kind regards, Areal Property Management Team', NOW());

-- Update search vectors for all inserted data
UPDATE evidence.documents 
SET search_vector = to_tsvector('english', 
    COALESCE(title, '') || ' ' || 
    COALESCE(content, '') || ' ' || 
    COALESCE(filename, '')
);

UPDATE evidence.emails 
SET search_vector = to_tsvector('english',
    COALESCE(subject, '') || ' ' || 
    COALESCE(body_text, '') || ' ' || 
    COALESCE(sender, '') || ' ' ||
    COALESCE(recipient, '')
);

-- Log the loading operation
INSERT INTO evidence.audit_log (operation, table_name, record_id, details, created_at) VALUES
('BULK_LOAD', 'documents', NULL, 'Loaded 5 sample VCAT evidence documents', NOW()),
('BULK_LOAD', 'emails', NULL, 'Loaded 3 sample VCAT evidence emails', NOW()),
('SEARCH_INDEX', 'all', NULL, 'Updated full-text search vectors for all evidence', NOW());

-- Display loading results
SELECT 'DOCUMENTS LOADED' as summary, COUNT(*) as count FROM evidence.documents
UNION ALL
SELECT 'EMAILS LOADED' as summary, COUNT(*) as count FROM evidence.emails;

-- Test search functionality
SELECT 'SEARCH TEST: water damage' as test_query, filename, title
FROM evidence.documents 
WHERE search_vector @@ to_tsquery('english', 'water & damage')
LIMIT 3;