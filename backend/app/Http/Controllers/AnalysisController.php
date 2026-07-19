<?php

namespace App\Http\Controllers;

use App\Models\Patient;
use App\Models\Analysis;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class AnalysisController extends Controller
{
    public function store(Request $request)
    {

    //Validation des données entrantes
        $request->validate([
            'image' => 'required|image',
            'name' => 'required|string',
            'email' => 'required|email',
            'date_naissance' => 'required|date',
            'sexe' => 'required|string',
        ]);
    //Récupère le patient existant (par email) ou en crée un nouveau
        $patient = Patient::firstOrCreate(
            ['email' => $request->input('email')],
            $request->only('name', 'date_naissance', 'sexe', 'adresse')
        );
//Appel de L'API FAST
        $response = Http::attach(
            'file',
            file_get_contents($request->file('image')->getRealPath()),
            $request->file('image')->getClientOriginalName()
        )->post('http://127.0.0.1:8000/predict');

        $result = $response->json();

        $imagePath = $request->file('image')->store('analyses', 'public');

        $heatmapData = explode(',', $result['heatmap'])[1];
        $heatmapName = 'analyses/' . Str::uuid() . '.png';
        Storage::disk('public')->put($heatmapName, base64_decode($heatmapData));

        $analysis = Analysis::create([
            'user_id' => $request->user()?->id ?? 1,
            'patient_id' => $patient->id,
            'image_path' => $imagePath,
            'heatmap_path' => $heatmapName,
            'label' => $result['label'],
        ]);

        return response()->json([
            'analysis' => $analysis,
            'score' => $result['score'],
        ]);
    }
}
