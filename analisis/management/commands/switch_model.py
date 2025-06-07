from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    """
    Command to switch the ML model and vectorizer used for prediction.
    Usage:
        python manage.py switch_model <model_name> [--vectorizer <vectorizer_name>]
    Example:
        switch to dummy model:
            python manage.py switch_model naivebayes_model_2.pkl --vectorizer vectorizer_2.pkl
        switch to real model:
            python manage.py switch_model naivebayes_model.pkl --vectorizer vectorizer.pkl
    """
    help = "Switch ML model and vectorizer used for prediction"

    def add_arguments(self, parser):
        parser.add_argument(
            "model_name",
            type=str,
            help="Model filename in model-ml/ (e.g. naivebayes_model.pkl or dummy_model.pkl)",
        )
        parser.add_argument(
            "--vectorizer",
            type=str,
            default=None,
            help="Vectorizer filename in model-ml/ (e.g. vectorizer.pkl or dummy_vectorizer.pkl)",
        )

    def handle(self, *args, **options):
        model_name = options["model_name"]
        vectorizer_name = options["vectorizer"]
        model_dir = os.path.join(settings.BASE_DIR, "analisis", "ml", "model-ml")

        # Switch model
        config_model_path = os.path.join(model_dir, "current_model.txt")
        model_path = os.path.join(model_dir, model_name)
        if not os.path.exists(model_path):
            self.stderr.write(self.style.ERROR(f"Model file {model_name} not found in {model_dir}"))
            return
        with open(config_model_path, "w") as f:
            f.write(model_name)
        self.stdout.write(self.style.SUCCESS(f"Switched model to {model_name}"))

        # Switch vectorizer (optional)
        if vectorizer_name:
            config_vectorizer_path = os.path.join(model_dir, "current_vectorizer.txt")
            vectorizer_path = os.path.join(model_dir, vectorizer_name)
            if not os.path.exists(vectorizer_path):
                self.stderr.write(self.style.ERROR(f"Vectorizer file {vectorizer_name} not found in {model_dir}"))
                return
            with open(config_vectorizer_path, "w") as f:
                f.write(vectorizer_name)
            self.stdout.write(self.style.SUCCESS(f"Switched vectorizer to {vectorizer_name}"))