import { format } from 'date-fns';

export const formatDate = (date: Date, dateFormat: string = 'MMMM dd, yyyy'): string => {
    return format(date, dateFormat);
};

export const formatDateRange = (startDate: Date, endDate: Date): string => {
    return `${formatDate(startDate)} - ${formatDate(endDate)}`;
};