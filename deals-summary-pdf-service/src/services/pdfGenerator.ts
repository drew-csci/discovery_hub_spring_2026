import { PDFDocument, rgb } from 'pdf-lib';

export class PdfGenerator {
    async generatePdf(dealData: {
        title: string;
        partnerNames: string[];
        stage: string;
        keyDates: { [key: string]: string };
        financialTerms: string;
    }): Promise<Uint8Array> {
        const pdfDoc = await PDFDocument.create();
        const page = pdfDoc.addPage([600, 400]);

        const { title, partnerNames, stage, keyDates, financialTerms } = dealData;

        page.drawText(`Deal Title: ${title}`, { x: 50, y: 350, size: 20, color: rgb(0, 0, 0) });
        page.drawText(`Partners: ${partnerNames.join(', ')}`, { x: 50, y: 320, size: 16, color: rgb(0, 0, 0) });
        page.drawText(`Stage: ${stage}`, { x: 50, y: 290, size: 16, color: rgb(0, 0, 0) });

        let yPosition = 260;
        for (const [key, value] of Object.entries(keyDates)) {
            page.drawText(`${key}: ${value}`, { x: 50, y: yPosition, size: 14, color: rgb(0, 0, 0) });
            yPosition -= 20;
        }

        page.drawText(`Financial Terms: ${financialTerms}`, { x: 50, y: yPosition, size: 16, color: rgb(0, 0, 0) });

        const pdfBytes = await pdfDoc.save();
        return pdfBytes;
    }
}