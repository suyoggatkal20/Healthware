import 'dart:convert';

class Create_patient {
  String _email, _password, _country_code, _phone;
  Patient _patient;
  List<Address> _address;
  List<Emergency_Contact> _emergency_contact;
  List<Map> _allergies;
  List<Map> _past_diseases;
  List<Map> _addictions;
  List<Weight> _weight;
  List<Height> _height;
  List<Map> _cholesterol;
  List<Map> _blood_pressure;
  List<Map> _glocose;

  Create_patient(
      this._email,
      this._password,
      this._country_code,
      this._phone,
      this._patient,
      this._address,
      this._emergency_contact,
      this._allergies,
      this._past_diseases,
      this._addictions,
      this._weight,
      this._height,
      this._cholesterol,
      this._blood_pressure,
      this._glocose);

  Map toJson() {
    return {
      'email': _email,
      'password': _password,
      'country_code': _country_code,
      'phone': _phone,
      'patient': this._patient.toJson(),
      'address': this._address.map((i) => i.toJson()).toList(),
      'emergency_contact':
          this._emergency_contact.map((i) => i.toJson()).toList(),
      'allergies': this._allergies,
      'past_diseases': this._past_diseases,
      'addictions': this._addictions,
      'weight': this._weight.map((i) => i.toJson()).toList(),
      'height': this._height.map((i) => i.toJson()).toList(),
      'cholesterol': this._cholesterol,
      'blood_pressure': this._blood_pressure,
      'glocose': this._glocose,
    };
  }
}

class Patient {
  String _first_name,
      _last_name,
      _dob,
      _gender,
      _married,
      _occupation,
      _blood_group,
      _education;

  Patient(this._first_name, this._last_name, this._dob, this._gender,
      this._married, this._occupation, this._blood_group, this._education);

  Map toJson(){
      return {
        'first_name': _first_name,
        'last_name': _last_name,
        'dob': _dob,
        'gender': _gender,
        'married': _married,
        'occupation': _occupation,
        'blood_group': _blood_group,
        'education': _education
      };
    }
}

class Address {
  String _house_no, _locality;

  Map toJson() => {"house_no": _house_no, "locality": _locality};

  Address(this._house_no, this._locality);
}

class Emergency_Contact {
  String _country_code, _phone_no, _relation;

  Emergency_Contact(this._country_code, this._phone_no, this._relation);

  Map toJson() => {
        "country_code": _country_code,
        "phone_no": _phone_no,
        "relation": _relation
      };
}

class Allergies {
  String _allergies, _description;

  Allergies(this._allergies, this._description);
  Map toJson() => {
        "allergies": _allergies,
        "description": _description,
      };
}

// ignore: camel_case_types
class Past_Diseases {
  String _past_diseases, _description;

  Past_Diseases(this._past_diseases, this._description);
  Map toJson() => {
        "past_diseases": _past_diseases,
        "description": _description,
      };
}

class Addictions {
  String _addiction;
  bool _current;

  Addictions(this._addiction, this._current);
  Map toJson() => {
        "addiction": _addiction,
        "current": _current,
      };
}

class Weight {
  String _weight, _date;

  Weight(this._weight, this._date);
  Map toJson() => {
        "weight": _weight,
        "date": _date,
      };
}

class Height {
  String _height, _date;

  Height(this._height, this._date);
  Map toJson() => {
        "height": _height,
        "date": _date,
      };
}

class Cholesterol {
  String _HDL, _LDL, _date;

  Cholesterol(this._HDL, this._LDL, this._date);
  Map toJson() => {
        "HDL": _HDL,
        "LDL": _LDL,
        "date": _date,
      };
}

// ignore: camel_case_types
class Blood_pressure {
  String _systolic, _diastolic, _date;

  Blood_pressure(this._systolic, this._diastolic, this._date);
  Map toJson() =>
      {"systolic": _systolic, "diastolic": _diastolic, "date": _date};
}

class Glocose {
  String _pre_meal, _post_meal, _date;

  Glocose(this._pre_meal, this._post_meal, this._date);

  Map toJson() =>
      {"pre_meal": _pre_meal, "post_meal": _post_meal, "date": _date};
}

void main() {
  Patient patient = Patient("suyog", "jhdsckj", "252/272/227", "M", "M", "Zak Marto", "A+", "PHD");

  List<Address> address = [Address("hgjh", "gfhjjh")];

  List<Emergency_Contact> emergency_contact = [
    Emergency_Contact("gjhjb", "gjkkj", "hghbj")
  ];

  List<Map> allergies = [{'allergies': 'ffgghh', 'description': 'rr'}, {'allergies': 'cffffghhh', 'description': 'fff'}, {'allergies': 'ffghhh', 'description': 'ff'}];

  List<Map> past_diseases = [{'past_diseases': 'fgyfggt', 'description': 'gg'}, {'past_diseases': 'gghujjgdff', 'description': 'ff'}, {'past_diseases': 'vvhhhg', 'description': 'eer'}];

  List<Map> addictions = [{'addiction': 'gtgyhjjj', 'current': true}, {'addiction': 'hhgfdddd', 'current': true}, {'addiction': 'fgh', 'current': true}];

  List<Weight> weight = [Weight("vhjbh", "bjhbj")];
  List<Height> height = [Height("gvhbv", "gjhjkn"), Height("gvhbv", "gjhjkn")];

  List<Map> cholesterol = [{'date': '2021-06-15', 'HDL': '55', 'LDL': '55'}, {'date': '2021-06-16', 'HDL': '56', 'LDL': '555'}, {'date': '2021-06-09', 'HDL': '999', 'LDL': '88'}];

  List<Map> blood_pressure = [{'date': '2021-06-09', 'systolic': '58', 'diastolic': '08'}, {'date': '2021-06-09', 'systolic': '96', 'diastolic': '55'}, {'date': '2021-06-09', 'systolic': '55', 'diastolic': '55'}];

  List<Map> glocose = [{'date': "2021-06-16", 'pre_meal': "888", 'post_meal': '88'}, {'date': '2021-06-16', 'pre_meal': '85', 'post_meal': '55'}, {'date': '2021-06-16', 'pre_meal': '85', 'post_meal': '88'}];




  Create_patient cc = Create_patient(
      "suyog@gmail.com",
      "hvhjbmnb",
      "+91",
      "8767564534",
      patient,
      address,
      emergency_contact,
      allergies,
      past_diseases,
      addictions,
      weight,
      height,
      cholesterol,
      blood_pressure,
      glocose);
  String jsonTags = jsonEncode(cc.toJson());
  print(jsonTags);
}