from django import forms

from .models import InventionDisclosure


class InventionDisclosureForm(forms.ModelForm):
    class Meta:
        model = InventionDisclosure
        fields = [
            "title",
            "summary",
            "inventors",
            "department",
            "technology_area",
            "novelty",
            "potential_applications",
            "funding_source",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
            "inventors": forms.Textarea(attrs={"rows": 4}),
            "novelty": forms.Textarea(attrs={"rows": 4}),
            "potential_applications": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "title": "Use the working title for the invention or technology.",
            "summary": "Briefly explain what was invented and the problem it solves.",
            "inventors": "Include all contributors in the order your office should contact them.",
            "novelty": "Describe what makes this invention new or distinct.",
            "potential_applications": "List the use cases, markets, or beneficiaries.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = True
            css_class = "input"
            if isinstance(field.widget, forms.Textarea):
                css_class = "textarea"
            elif isinstance(field.widget, forms.Select):
                css_class = "select"
            field.widget.attrs.setdefault("class", css_class)

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 10:
            raise forms.ValidationError("Enter a title with at least 10 characters.")
        return title

    def clean_department(self):
        department = self.cleaned_data["department"].strip()
        if len(department) < 3:
            raise forms.ValidationError("Enter the department or lab name.")
        return department

    def clean_funding_source(self):
        funding_source = self.cleaned_data["funding_source"].strip()
        if len(funding_source) < 3:
            raise forms.ValidationError("Enter the funding source for this work.")
        return funding_source

    def clean_inventors(self):
        inventors = self.cleaned_data["inventors"]
        tokens = [token.strip() for token in inventors.replace("\n", ",").split(",") if token.strip()]
        if len(tokens) < 1:
            raise forms.ValidationError("Enter at least one inventor.")
        if any(len(token.split()) < 2 for token in tokens):
            raise forms.ValidationError("Each inventor should include a first and last name.")
        return "\n".join(tokens)

    def clean(self):
        cleaned_data = super().clean()
        summary = (cleaned_data.get("summary") or "").strip()
        novelty = (cleaned_data.get("novelty") or "").strip()
        potential_applications = (cleaned_data.get("potential_applications") or "").strip()

        if summary and len(summary) < 50:
            self.add_error("summary", "Provide a fuller summary with at least 50 characters.")
        if novelty and len(novelty) < 30:
            self.add_error("novelty", "Describe the novelty in at least 30 characters.")
        if potential_applications and len(potential_applications) < 20:
            self.add_error(
                "potential_applications",
                "Describe at least one realistic application in 20 characters or more.",
            )
        if summary and novelty and summary.lower() == novelty.lower():
            self.add_error("novelty", "Novelty should add detail beyond the general summary.")

        return cleaned_data
