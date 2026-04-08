import { Request, Response } from 'express';
import { DealController } from '../src/controllers/dealController';
import { PdfGenerator } from '../src/services/pdfGenerator';

describe('DealController', () => {
    let dealController: DealController;

    beforeEach(() => {
        dealController = new DealController();
    });

    describe('createDealSummary', () => {
        it('should generate a PDF summary and set correct headers', async () => {
            const pdfBytes = Buffer.from('%PDF-1.4');
            jest.spyOn(PdfGenerator.prototype, 'generatePdf').mockResolvedValue(pdfBytes);

            const req = {
                body: {
                    title: 'New Partnership',
                    partnerNames: ['Partner A', 'Partner B'],
                    stage: 'Negotiation',
                    keyDates: { startDate: '2026-01-01', endDate: '2026-12-31' },
                    financialTerms: 'USD 500k'
                }
            } as unknown as Request;

            const res = {
                set: jest.fn().mockReturnThis(),
                send: jest.fn(),
                status: jest.fn().mockReturnThis()
            } as unknown as Response;

            await dealController.createDealSummary(req, res);

            expect(PdfGenerator.prototype.generatePdf).toHaveBeenCalledWith(expect.objectContaining({ title: 'New Partnership' }));
            expect(res.set).toHaveBeenCalledWith(expect.objectContaining({ 'Content-Type': 'application/pdf' }));
            expect(res.send).toHaveBeenCalledWith(pdfBytes);
        });

        it('should return 400 when deal data is invalid', async () => {
            const req = { body: { title: '', partnerNames: [], stage: '', keyDates: {}, financialTerms: '' } } as unknown as Request;
            const res = { set: jest.fn(), send: jest.fn(), status: jest.fn().mockReturnThis() } as unknown as Response;

            await dealController.createDealSummary(req, res);

            expect(res.status).toHaveBeenCalledWith(400);
            expect(res.send).toHaveBeenCalledWith('Invalid deal data');
        });
    });
});