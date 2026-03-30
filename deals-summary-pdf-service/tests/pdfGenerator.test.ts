import { PdfGenerator } from '../src/services/pdfGenerator';
import { Deal } from '../src/models/deal';

describe('PdfGenerator', () => {
    let pdfGenerator: PdfGenerator;

    beforeEach(() => {
        pdfGenerator = new PdfGenerator();
    });

    it('should generate a PDF with the correct deal summary', async () => {
        const dealData = {
            title: 'Strategic Partnership',
            partnerNames: ['Company A', 'Company B'],
            stage: 'Negotiation',
            keyDates: {
                startDate: '2023-01-01',
                endDate: '2023-12-31',
            },
            financialTerms: 'USD 1,000,000, 50% upfront',
        };

        const pdfBuffer = await pdfGenerator.generatePdf(dealData);
        
        expect(pdfBuffer).toBeInstanceOf(Buffer);
        // Additional checks can be added here to verify the content of the PDF
    });

    it('should generate a PDF even when financial terms are empty string', async () => {
        const dealData = {
            title: 'Limited Data Deal',
            partnerNames: ['Company A'],
            stage: 'Initial',
            keyDates: { startDate: '2026-03-01' },
            financialTerms: ''
        };

        const pdfBuffer = await pdfGenerator.generatePdf(dealData as any);
        expect(pdfBuffer).toBeInstanceOf(Buffer);
        expect(pdfBuffer.length).toBeGreaterThan(0);
    });
});