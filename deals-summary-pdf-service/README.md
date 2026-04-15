# Deals Summary PDF Service

This project provides a service for generating PDF summaries of deals, including essential details such as deal title, partner names, stage, key dates, and financial terms. The generated PDF can be easily shared with stakeholders.

## Project Structure

```
deals-summary-pdf-service
├── src
│   ├── index.ts               # Entry point of the application
│   ├── controllers
│   │   └── dealController.ts   # Logic for generating deal summaries
│   ├── routes
│   │   └── dealRoutes.ts       # API routes for deal summaries
│   ├── services
│   │   └── pdfGenerator.ts      # PDF generation logic
│   ├── models
│   │   └── deal.ts             # Deal data structure
│   └── utils
│       └── dateFormatter.ts     # Utility functions for date formatting
├── tests
│   ├── dealController.test.ts   # Unit tests for DealController
│   └── pdfGenerator.test.ts      # Unit tests for PdfGenerator
├── package.json                 # Project dependencies and scripts
├── tsconfig.json                # TypeScript configuration
└── README.md                    # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd deals-summary-pdf-service
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   npm start
   ```

## Usage

To generate a deal summary PDF, send a POST request to the `/deals` endpoint with the deal data in the request body. The service will respond with the generated PDF.

## Purpose

The Deals Summary PDF Service aims to streamline the process of creating and sharing deal summaries, ensuring that stakeholders have quick access to important deal information in a professional format.