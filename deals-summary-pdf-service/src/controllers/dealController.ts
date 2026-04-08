import { Request, Response } from 'express';
import { PdfGenerator } from '../services/pdfGenerator';
import { Deal } from '../models/deal';

export class DealController {
    private pdfGenerator: PdfGenerator;

    constructor() {
        this.pdfGenerator = new PdfGenerator();
    }

    public createDealSummary(req: Request, res: Response): void {
        const dealData: Deal = req.body;

        // Validate deal data
        if (!this.validateDealData(dealData)) {
            res.status(400).send('Invalid deal data');
            return;
        }

        // Generate PDF
        const pdfBuffer = this.pdfGenerator.generatePdf(dealData);

        // Set response headers for PDF download
        res.set({
            'Content-Type': 'application/pdf',
            'Content-Disposition': `attachment; filename="${dealData.title}-summary.pdf"`,
            'Content-Length': pdfBuffer.length
        });

        // Send PDF as response
        res.send(pdfBuffer);
    }

    private validateDealData(dealData: Deal): boolean {
        return dealData.title && dealData.partnerNames && dealData.stage && dealData.keyDates && dealData.financialTerms;
    }
}