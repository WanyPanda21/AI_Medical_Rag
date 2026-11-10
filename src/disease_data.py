
DISEASES = [
    {
        "name": "Common Cold",
        "category": "Respiratory",
        "symptoms": ["Runny nose", "Sneezing", "Sore throat", "Cough", "Mild fever"],
        "medicines": ["Paracetamol", "Saline nasal spray"],
        "precautions": "Usually viral. Antibiotics do not treat common cold."
    },
    {
        "name": "Influenza",
        "category": "Respiratory",
        "symptoms": ["High fever", "Muscle pain", "Headache", "Fatigue", "Dry cough"],
        "medicines": ["Paracetamol", "Oseltamivir when clinically indicated"],
        "precautions": "Antiviral treatment may be appropriate for eligible patients."
    },
    {
        "name": "COVID-19",
        "category": "Infectious",
        "symptoms": ["Fever", "Cough", "Fatigue", "Loss of smell", "Breathing difficulty"],
        "medicines": ["Paracetamol", "Clinician-selected antiviral treatment"],
        "precautions": "Breathing difficulty requires urgent assessment."
    },
    {
        "name": "Asthma",
        "category": "Respiratory",
        "symptoms": ["Wheezing", "Shortness of breath", "Chest tightness", "Cough"],
        "medicines": ["Inhaled corticosteroids", "Prescribed bronchodilators"],
        "precautions": "Severe breathing difficulty is an emergency."
    },
    {
        "name": "Pneumonia",
        "category": "Respiratory",
        "symptoms": ["Fever", "Cough", "Chest pain", "Shortness of breath"],
        "medicines": ["Clinician-selected antibiotics for bacterial pneumonia"],
        "precautions": "Treatment depends on the cause and severity."
    },
    {
        "name": "Tuberculosis",
        "category": "Infectious",
        "symptoms": ["Persistent cough", "Night sweats", "Weight loss", "Fever"],
        "medicines": ["Combination anti-tuberculosis medicines"],
        "precautions": "Requires testing and supervised treatment."
    },
    {
        "name": "Allergic Rhinitis",
        "category": "Allergy",
        "symptoms": ["Sneezing", "Runny nose", "Itchy eyes", "Nasal congestion"],
        "medicines": ["Antihistamines", "Intranasal corticosteroids"],
        "precautions": "Identify and reduce exposure to allergens."
    },
    {
        "name": "Sinusitis",
        "category": "Respiratory",
        "symptoms": ["Facial pressure", "Nasal congestion", "Headache", "Nasal discharge"],
        "medicines": ["Saline irrigation", "Intranasal corticosteroids"],
        "precautions": "Antibiotics are appropriate only in selected bacterial cases."
    },
    {
        "name": "Bronchitis",
        "category": "Respiratory",
        "symptoms": ["Cough", "Mucus", "Chest discomfort", "Fatigue"],
        "medicines": ["Symptom-relieving medicines when appropriate"],
        "precautions": "Most acute cases are viral."
    },
    {
        "name": "COPD",
        "category": "Respiratory",
        "symptoms": ["Chronic cough", "Breathlessness", "Wheezing", "Sputum"],
        "medicines": ["Prescribed bronchodilators"],
        "precautions": "Requires long-term respiratory care."
    },
    {
        "name": "Hypertension",
        "category": "Cardiovascular",
        "symptoms": ["Often no symptoms", "Sometimes headache", "Dizziness"],
        "medicines": ["ACE inhibitors", "ARBs", "Calcium channel blockers"],
        "precautions": "Requires blood pressure monitoring."
    },
    {
        "name": "Type 1 Diabetes",
        "category": "Endocrine",
        "symptoms": ["Excessive thirst", "Frequent urination", "Weight loss", "Fatigue"],
        "medicines": ["Insulin"],
        "precautions": "Insulin is essential."
    },
    {
        "name": "Type 2 Diabetes",
        "category": "Endocrine",
        "symptoms": ["Increased thirst", "Frequent urination", "Fatigue", "Blurred vision"],
        "medicines": ["Metformin", "SGLT2 inhibitors", "GLP-1 receptor agonists"],
        "precautions": "Treatment depends on kidney function and cardiovascular risk."
    },
    {
        "name": "Hypothyroidism",
        "category": "Endocrine",
        "symptoms": ["Fatigue", "Weight gain", "Cold intolerance", "Constipation"],
        "medicines": ["Levothyroxine"],
        "precautions": "Requires thyroid function monitoring."
    },
    {
        "name": "Hyperthyroidism",
        "category": "Endocrine",
        "symptoms": ["Weight loss", "Palpitations", "Tremors", "Heat intolerance"],
        "medicines": ["Methimazole", "Selected beta blockers"],
        "precautions": "Requires thyroid testing and specialist assessment."
    },
    {
        "name": "Iron Deficiency Anemia",
        "category": "Blood",
        "symptoms": ["Fatigue", "Pale skin", "Dizziness", "Weakness"],
        "medicines": ["Oral iron preparations"],
        "precautions": "Investigate the cause of iron deficiency."
    },
    {
        "name": "Vitamin B12 Deficiency",
        "category": "Nutritional",
        "symptoms": ["Fatigue", "Tingling", "Numbness", "Memory problems"],
        "medicines": ["Vitamin B12 replacement"],
        "precautions": "Neurological symptoms need timely evaluation."
    },
    {
        "name": "Vitamin D Deficiency",
        "category": "Nutritional",
        "symptoms": ["Bone pain", "Muscle weakness"],
        "medicines": ["Vitamin D replacement when confirmed"],
        "precautions": "Avoid excessive supplementation."
    },
    {
        "name": "Migraine",
        "category": "Neurological",
        "symptoms": ["Throbbing headache", "Nausea", "Light sensitivity", "Sound sensitivity"],
        "medicines": ["Selected NSAIDs", "Triptans"],
        "precautions": "Sudden severe headache requires urgent assessment."
    },
    {
        "name": "Epilepsy",
        "category": "Neurological",
        "symptoms": ["Recurrent seizures", "Altered awareness", "Unusual sensations"],
        "medicines": ["Levetiracetam", "Lamotrigine"],
        "precautions": "Medicine selection depends on seizure type."
    },
    {
        "name": "Parkinson's Disease",
        "category": "Neurological",
        "symptoms": ["Tremor", "Slowness of movement", "Muscle stiffness"],
        "medicines": ["Levodopa with carbidopa"],
        "precautions": "Requires neurological monitoring."
    },
    {
        "name": "Alzheimer's Disease",
        "category": "Neurological",
        "symptoms": ["Memory loss", "Confusion", "Difficulty with daily activities"],
        "medicines": ["Donepezil", "Selected cognitive symptom treatments"],
        "precautions": "Requires specialist evaluation."
    },
    {
        "name": "Depression",
        "category": "Mental Health",
        "symptoms": ["Persistent sadness", "Loss of interest", "Sleep changes", "Low energy"],
        "medicines": ["SSRIs", "SNRIs"],
        "precautions": "Psychotherapy is also an important treatment."
    },
    {
        "name": "Generalized Anxiety Disorder",
        "category": "Mental Health",
        "symptoms": ["Excessive worry", "Restlessness", "Muscle tension", "Sleep disturbance"],
        "medicines": ["SSRIs", "SNRIs"],
        "precautions": "Psychological therapy is commonly recommended."
    },
    {
        "name": "Insomnia",
        "category": "Sleep",
        "symptoms": ["Difficulty falling asleep", "Frequent waking", "Daytime tiredness"],
        "medicines": ["Selected short-term sleep medicines when prescribed"],
        "precautions": "Cognitive behavioral therapy for insomnia is preferred."
    },
    {
        "name": "GERD",
        "category": "Digestive",
        "symptoms": ["Heartburn", "Acid regurgitation", "Chest discomfort"],
        "medicines": ["Proton pump inhibitors", "H2 blockers"],
        "precautions": "Difficulty swallowing requires assessment."
    },
    {
        "name": "Peptic Ulcer Disease",
        "category": "Digestive",
        "symptoms": ["Upper abdominal pain", "Nausea", "Bloating"],
        "medicines": ["Proton pump inhibitors", "H. pylori eradication treatment when confirmed"],
        "precautions": "Treatment depends on testing and cause."
    },
    {
        "name": "Gastritis",
        "category": "Digestive",
        "symptoms": ["Upper abdominal discomfort", "Nausea", "Bloating"],
        "medicines": ["Proton pump inhibitors"],
        "precautions": "Persistent symptoms require evaluation."
    },
    {
        "name": "Irritable Bowel Syndrome",
        "category": "Digestive",
        "symptoms": ["Abdominal pain", "Bloating", "Diarrhea", "Constipation"],
        "medicines": ["Selected antispasmodics", "Fiber supplements"],
        "precautions": "Blood in stool requires investigation."
    },
    {
        "name": "Inflammatory Bowel Disease",
        "category": "Digestive",
        "symptoms": ["Chronic diarrhea", "Abdominal pain", "Blood in stool", "Weight loss"],
        "medicines": ["Mesalamine", "Selected biologic medicines"],
        "precautions": "Requires gastroenterology supervision."
    },
    {
        "name": "Acute Diarrhea",
        "category": "Digestive",
        "symptoms": ["Loose stools", "Abdominal cramps", "Nausea"],
        "medicines": ["Oral rehydration solution", "Cause-specific treatment"],
        "precautions": "Prevent dehydration."
    },
    {
        "name": "Constipation",
        "category": "Digestive",
        "symptoms": ["Hard stools", "Straining", "Infrequent bowel movements"],
        "medicines": ["Fiber supplements", "Polyethylene glycol"],
        "precautions": "Severe abdominal pain or vomiting needs assessment."
    },
    {
        "name": "Hemorrhoids",
        "category": "Digestive",
        "symptoms": ["Rectal bleeding", "Itching", "Pain", "Swelling"],
        "medicines": ["Fiber supplements", "Selected topical treatments"],
        "precautions": "Rectal bleeding needs evaluation."
    },
    {
        "name": "Urinary Tract Infection",
        "category": "Urinary",
        "symptoms": ["Burning urination", "Frequent urination", "Lower abdominal discomfort"],
        "medicines": ["Clinician-selected antibiotics"],
        "precautions": "Fever or flank pain may indicate kidney infection."
    },
    {
        "name": "Kidney Stones",
        "category": "Urinary",
        "symptoms": ["Severe flank pain", "Blood in urine", "Nausea", "Vomiting"],
        "medicines": ["Selected pain relievers", "Selected medical expulsive therapy"],
        "precautions": "Fever with suspected obstruction is an emergency."
    },
    {
        "name": "Chronic Kidney Disease",
        "category": "Urinary",
        "symptoms": ["Swelling", "Fatigue", "Changes in urination"],
        "medicines": ["ACE inhibitors or ARBs when indicated"],
        "precautions": "Requires kidney function monitoring."
    },
    {
        "name": "Osteoarthritis",
        "category": "Musculoskeletal",
        "symptoms": ["Joint pain", "Stiffness", "Reduced movement"],
        "medicines": ["Topical NSAIDs", "Selected pain relievers"],
        "precautions": "Exercise and physical therapy can help."
    },
    {
        "name": "Rheumatoid Arthritis",
        "category": "Musculoskeletal",
        "symptoms": ["Joint swelling", "Morning stiffness", "Joint pain"],
        "medicines": ["Methotrexate", "Other disease-modifying medicines"],
        "precautions": "Requires rheumatology supervision."
    },
    {
        "name": "Gout",
        "category": "Musculoskeletal",
        "symptoms": ["Sudden joint pain", "Redness", "Swelling"],
        "medicines": ["Selected NSAIDs", "Colchicine", "Allopurinol"],
        "precautions": "A first hot swollen joint needs medical assessment."
    },
    {
        "name": "Osteoporosis",
        "category": "Musculoskeletal",
        "symptoms": ["Often no symptoms until fracture", "Fragility fractures"],
        "medicines": ["Bisphosphonates"],
        "precautions": "Treatment depends on fracture risk."
    },
    {
        "name": "Eczema",
        "category": "Skin",
        "symptoms": ["Itchy skin", "Dryness", "Redness", "Rash"],
        "medicines": ["Moisturizers", "Topical corticosteroids when indicated"],
        "precautions": "Avoid triggers and watch for infection."
    },
    {
        "name": "Psoriasis",
        "category": "Skin",
        "symptoms": ["Scaly plaques", "Red skin", "Itching"],
        "medicines": ["Topical corticosteroids", "Vitamin D analogues"],
        "precautions": "Treatment depends on severity."
    },
    {
        "name": "Acne",
        "category": "Skin",
        "symptoms": ["Pimples", "Blackheads", "Whiteheads", "Inflamed lesions"],
        "medicines": ["Benzoyl peroxide", "Topical retinoids"],
        "precautions": "Pregnancy considerations apply to some treatments."
    },
    {
        "name": "Fungal Skin Infection",
        "category": "Skin",
        "symptoms": ["Itchy rash", "Scaling", "Ring-shaped patches"],
        "medicines": ["Clotrimazole", "Terbinafine"],
        "precautions": "Treatment depends on infection site."
    },
    {
        "name": "Scabies",
        "category": "Skin",
        "symptoms": ["Severe itching", "Night-time itching", "Small skin burrows"],
        "medicines": ["Permethrin topical treatment"],
        "precautions": "Close contacts may also need treatment."
    },
    {
        "name": "Conjunctivitis",
        "category": "Eye",
        "symptoms": ["Red eye", "Discharge", "Itching", "Tearing"],
        "medicines": ["Lubricating eye drops", "Cause-specific prescription treatments"],
        "precautions": "Eye pain or vision changes need urgent assessment."
    },
    {
        "name": "Glaucoma",
        "category": "Eye",
        "symptoms": ["Often no early symptoms", "Gradual vision loss"],
        "medicines": ["Latanoprost", "Selected pressure-lowering eye drops"],
        "precautions": "Requires ophthalmology monitoring."
    },
    {
        "name": "Dengue",
        "category": "Infectious",
        "symptoms": ["High fever", "Severe body aches", "Rash", "Headache"],
        "medicines": ["Paracetamol when appropriate", "Clinically guided fluids"],
        "precautions": "Avoid aspirin and NSAIDs when dengue is suspected."
    },
    {
        "name": "Malaria",
        "category": "Infectious",
        "symptoms": ["Fever", "Chills", "Sweating", "Headache"],
        "medicines": ["Species-specific antimalarial medicines"],
        "precautions": "Requires prompt testing and treatment."
    },
    {
        "name": "Typhoid Fever",
        "category": "Infectious",
        "symptoms": ["Persistent fever", "Headache", "Abdominal discomfort", "Weakness"],
        "medicines": ["Antibiotics selected according to susceptibility"],
        "precautions": "Requires clinical evaluation and testing."
    }
]


# Validate dataset automatically
assert len(DISEASES) == 50, (
    f"Dataset must contain exactly 50 diseases. "
    f"Found {len(DISEASES)}"
)

print(f"Medical dataset loaded: {len(DISEASES)} diseases")
