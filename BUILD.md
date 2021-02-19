# Building a package

## Build Distrubition

```python
python setup.py sdist bdist_wheel
```

## Upload

```python
twine upload -u __token__ --repository testpypi dist/*
```

