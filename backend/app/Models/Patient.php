<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Patient extends Model
{
    protected $fillable = [
        'name', 
        'email', 
        'date_naissance', 
        'sexe', 
        'adresse'
    ];
}
